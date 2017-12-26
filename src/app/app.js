import React from 'react';
import ReactDOM from 'react-dom';
import Editor from './Editor';
import Output from './Output';
require('codemirror/lib/codemirror.css');

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result: '',
        }
    }

    evaluate = (code) => {
        fetch('/evaluate', {code: code})
        .then((res) => {
            this.setState({
                result: res['result']
            })
        })
        .catch((err) => {
            this.setState({
                result: res['err']
            })
        });
    }

    render() {
        return <div>
            <Editor evaluate={this.evaluate}/>
            <Output result={this.state.result}>sdg</Output>
        </div>
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);