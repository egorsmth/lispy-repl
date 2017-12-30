import React from 'react';
import CodeMirror from 'react-codemirror'
require('codemirror/mode/commonlisp/commonlisp');

export default class Editor extends React.Component {
   
    constructor(props) {
        super(props);
        this.state = {
            code: '(+ 3 4)',
        };
    }

    updateCode = (newCode) => {
        this.setState({
            code: newCode,
        })
    }

    evaluate = (e) => {
        e.preventDefault();
        const form = new FormData()
        form.append('code', this.state.code)
        this.props.evaluate(form)
    }

    render() {
        const options = {
            lineNumbers: true
        }
        const style = {
             width: '45%',
             float: 'left',
             height: '100%',
        }
        return <div style={style}>
            <CodeMirror
                value={this.state.code}
                options={{
                    lineNumbers: true,
                    mode: 'commonlisp',
                    theme: 'material',
                    lineSeparator: '\n'
                }}
                onChange={this.updateCode}
            />
            <button id='eval-btn' onClick={this.evaluate}>Evaluate</button>
        </div>
    }
}