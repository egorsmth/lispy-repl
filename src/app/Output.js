import React from 'react';

export default class Output extends React.Component {

    render() {
        const style = {
            height: '250px',
            'background-color': '#ccccff',
            'font-size': '25px',
        }

        return <div style={style}>
            {this.props.children}
        </div>
    }
}