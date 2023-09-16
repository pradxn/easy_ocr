const { v4: uuidv4 } = require('uuid');
const readline = require('readline');
const openai = require('openai');
const fs = require('fs');

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function extract_text(response, extract_by="WORD") {
  const line_text = [];
  response.Blocks.forEach((block) => {
    if (block.BlockType === extract_by) {
      line_text.push(block.Text);
    }
  });
  return line_text;
}

function map_word_id(response) {
  const word_map = {};
  response.Blocks.forEach((block) => {
    if (block.BlockType === "WORD") {
      word_map[block.Id] = block.Text;
    }
    if (block.BlockType === "SELECTION_ELEMENT") {
      word_map[block.Id] = block.SelectionStatus;
    }
  });
  return word_map;
}

function extract_table_info(response, word_map) {
  let row = [];
  const table = {};
  let ri = 0;
  let flag = false;

  response.Blocks.forEach((block) => {
    if (block.BlockType === "TABLE") {
      const key = `table_${uuidv4()}`;
      let temp_table = [];
      ri = 0;
      flag = false;
      table[key] = temp_table;
    }
    if (block.BlockType === "CELL") {
      if (block.RowIndex !== ri) {
        flag = true;
        row = [];
        ri = block.RowIndex;
      }
      if (block.Relationships) {
        block.Relationships.forEach((relation) => {
          if (relation.Type === "CHILD") {
            row.push(relation.Ids.map(id => word_map[id]).join(" "));
          }
        });
      } else {
        row.push(" ");
      }
      if (flag) {
        table[Object.keys(table)[Object.keys(table).length - 1]].push(row);
        flag = false;
      }
    }
  });
  return table;
}

function get_key_map(response, word_map) {
  const key_map = {};
  response.Blocks.forEach((block) => {
    if (block.BlockType === "KEY_VALUE_SET" && block.EntityTypes.includes("KEY")) {
      block.Relationships.forEach((relation) => {
        if (relation.Type === "VALUE") {
          value_id = relation.Ids;
        }
        if (relation.Type === "CHILD") {
          const v = relation.Ids.map(id => word_map[id]).join(" ");
          key_map[v] = value_id;
        }
      });
    }
  });
  return key_map;
}

function get_value_map(response, word_map) {
  const value_map = {};
  response.Blocks.forEach((block) => {
    if (block.BlockType === "KEY_VALUE_SET" && block.EntityTypes.includes("VALUE")) {
      if (block.Relationships) {
        block.Relationships.forEach((relation) => {
          if (relation.Type === "CHILD") {
            const v = relation.Ids.map(id => word_map[id]).join(" ");
            value_map[block.Id] = v;
          }
        });
      } else {
        value_map[block.Id] = "VALUE_NOT_FOUND";
      }
    }
  });
  return value_map;
}

function get_kv_map(key_map, value_map) {
  const final_map = {};
  Object.entries(key_map).forEach(([k, v]) => {
    final_map[k] = v.map(id => value_map[id]).join("");
  });
  return final_map;
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
console.log('\n');

const response = require('./analyzeDocResponse.json');

const raw_text = extract_text(response, extract_by="LINE");
const word_map = map_word_id(response);
const table = extract_table_info(response, word_map);
const key_map = get_key_map(response);
const value_map = get_value_map(response, word_map);
const kv_map = get_kv_map(key_map, value_map);

console.log("Raw text:\n", raw_text);
console.log("\nTable information:\n", table);
console.log("\nKey-Value Map:\n", kv_map);

console.log(raw_text);
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function print_table(data) {
  for (const [key, values] of Object.entries(data)) {
    console.log("\n");
    for (const value of values) {
      const row = value.slice(0, 4).map(x => String(x).padEnd(20)).join("|");
      console.log(row);
    }
  }
}

print_table(table);

const strTable = JSON.stringify(table);

function dataParsed(params, final_map) {
    openai.api_key = fs.readFileSync('key.txt', 'utf8').trim();
    const prompt = `Values of ${params} from ${JSON.stringify(final_map)}:, comma and line separated`;
    return openai.Completion.create({
      engine: 'text-davinci-002',
      prompt: prompt,
      temperature: 0.7,
      max_tokens: 2048,
    })
    .then(response => {
      return response.choices[0].text.trim();
    })
    .catch(error => {
      console.log(error);
    });
  }

  const MongoClient = require('mongodb').MongoClient;
  const uri = "mongodb+srv://pradeepvajrala:M6dGJfkIZJVhPCZU@cluster0.qu3shkb.mongodb.net/";
  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
  
  const dbName = "Omerald_database";
  const collectionName = "Omerald_collection";
  
  let keyInput = prompt('Document name: ');
  console.log('\n');
  let key = keyInput;
  let original_string = outputParsed;
  //original_string = "NEUTROPHILS: 57.3%, LYMPHOCYTES: 30.2%, EOSINOPHILS: 3.5%, MONOCYTES: 7.4%, BASOPHILS: 1.6%, NEUTROPHILS: 2292 cells/cu.mm, LYMPHOCYTES: 1208 cells/cu.mm, EOSINOPHILS: 140 cells/cu.mm, MONOCYTES: 296 cells/cu.mm, BASOPHILS: 64 cells/cu.mm"
  let split_string = original_string.split(",");
  let result_string = split_string.map(s => `"${s.trim()}"`).join(", ");
  let value = result_string.split(", ").map(s => s.trim().replace(/"/g, ""));
  
  //console.log(value);
  
  client.connect(err => {
    const collection = client.db(dbName).collection(collectionName);
    const document = {[key]: value};
    collection.insertOne(document, (err, result) => {
      if (err) throw err;
      console.log(`Save this id for future reference: ${result.insertedId}`);
      console.log('\n');
      let object_id_str = prompt('Enter reference id: ');
      console.log('\n');
      let object_id = new ObjectId(object_id_str);
      collection.findOne({"_id": object_id}, (err, document) => {
        if (err) throw err;
        console.log(document);
        client.close();
      });
    });
  });

  if (document) {
    let value = document[key];
    console.log("{:<15}{}".format("Key", "Value"));
    console.log('--------------------');
    if (typeof value === "string") {
      console.log("{:<15}{}".format(key, value));
      console.log('\n');
    } else {
      for (let v of value) {
        if (v.includes(":")) {
          let [k, val] = v.split(": ");
          console.log("{:<15}{}".format(k, val));
        } else {
          console.log("{:<15}{}".format(key, v));
          console.log('\n');
        }
      }
    }
  } else {
    console.log("No document found with the given id.");
  }
  
  console.log('\n');

  