import React from 'react';

export default class Output extends React.Component {

    render() {
        return <div id="output">
            {this.props.children}
        </div>
    }
}