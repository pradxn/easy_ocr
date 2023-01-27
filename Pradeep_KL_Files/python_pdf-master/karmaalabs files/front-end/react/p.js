import React from "react";
import axios from "axios";

class DisplayData extends React.Component{
     state = {
        posts: []
    };

    componentDidMount() {
        this.getPosts();
    }

    getPosts() {
        axios
        .get('http://127.0.0.1:8000/api/')
        .then(res => {
            this.setState({ posts: res.data });
        })
        .catch(err => {
            console.log(err);
        });
    }
    render() {
        return (
            <div className={'container'}>
                {this.state.posts.map(item => (
                    <div key={item.id}>
                        {/*<h2>{item.person}</h2>*/}
                        <h4>{item.title}</h4>
                        <h4>{item.body}</h4>
                        <h4>{item.created_at}</h4>
                        <p>...</p>
                    </div>
                ))}
            </div>
        );
    }
}
export default DisplayData;