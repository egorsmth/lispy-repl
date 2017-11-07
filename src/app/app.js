import React from 'react';
import ReactDOM from 'react-dom';
import Editor from './editor/Editor';

ReactDOM.render(
    <Editor message="React Demo" />,
    document.querySelector( '.js-app' )
);