import React from 'react';

export default class Output extends React.Component {
    render() {
        return <div>
            {this.props.children}
        </div>
    }
}