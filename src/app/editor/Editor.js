import React from 'react';

class Editor extends React.Component {
   render() {
        return (
            <div>{this.props.message} editor</div>
        );
   }
}

export default Editor