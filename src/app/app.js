import React from 'react';
import ReactDOM from 'react-dom';
import Editor from './Editor';
import Output from './Output';
require('codemirror/lib/codemirror.css');

class App extends React.Component {
    render() {
        return <div>
            <Editor />
            <Output>sdg</Output>
        </div>
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app')
);