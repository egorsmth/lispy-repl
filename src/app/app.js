import React from 'react';
import ReactDOM from 'react-dom';
import Editor from './Editor';
import Output from './Output';
import Help from './Help';
import './editor.css';
import Cookies from 'js-cookie'

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result: '',
        }
    }

    evaluate = (code) => {
        console.log(code)
        let headers = {
            "X-CSRFToken": Cookies.get('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, application/xml, text/plain, text/html, *.*',
        }

        fetch('/evaluate/', {
             method: 'post',
             credentials: "same-origin",
             headers: headers,
             body: code,
        }).then((resp) => {
            console.log(resp)
            return resp.json()
        }).then((resp) => {
             this.setState({
                 result: resp.out
             })
        }).catch((ex) => {
             console.error(`fetch #{url} failed`, ex);
             this.setState({
                result: ex.toString()
            })
        });

    }

    render() {
        const style = {
            width: '49%',
            float: 'right',
        }

        return [
            <Editor evaluate={this.evaluate}/>,
            <div style={style}>
                <Output>{this.state.result}</Output>
                <Help />
            </div>

        ]
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);