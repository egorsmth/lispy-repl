import React from 'react';

export default class Output extends React.Component {
    render() {
        return <div style={{width: '49%', float: 'right'}}>
            {this.props.children}
        </div>
    }
}