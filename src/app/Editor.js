import React from 'react';
import CodeMirror from 'react-codemirror'

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
        return <div style={{width: '49%', float: 'left'}}>
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
            <button onClick={this.evaluate}>Evaluate</button>
        </div>
    }
}