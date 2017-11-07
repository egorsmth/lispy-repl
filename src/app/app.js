import React from 'react';
import ReactDOM from 'react-dom';

class SimpleComponent extends React.Component {
   render() {
        return (
            <div>{this.props.message}</div>
        );
   }
}

ReactDOM.render(
    <SimpleComponent message="React Demo" />,
    document.querySelector( '.js-app' )
);