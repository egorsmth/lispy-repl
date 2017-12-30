import ReactDOM from 'react-dom';
import React from 'react';
import ReactMarkdown from 'react-markdown';

export default class Help extends React.Component {
    render() {
        const input = `
### Docs
arithmetic:\n
    (* x y)\n
    (+ x y)\n
    (- x y)\n
    (/ x y)

predicates:\n
    (> x y)\n
    (< x y)\n
    (== x y)

define variable 'a' that equals 5:\n
    (def a 5)

define function root:\n
    (defn root (x) (* x x))\n
or with lambda:\n
    (def root (lambda (x) (* x x)))

function that returns function:\n
    (defn x () (\n
        (defn y (b) (* b b))\n
        \`y\n
    ))\n
    ((x) 5)  // call function x and pass 5 nj returned function\n
`

        return <ReactMarkdown source={input} />
    }
}
