---
layout: post
title:  "ReactJs reference notes"
author: Vikas Sharma
date:   2023-10-12 12:35:00 +0530
image: assets/images/react-reference-notes.jpeg
categories: [technical, frontend]
featured: true
show_preview: false
---

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@i_vikassharma">
<meta name="twitter:creator" content="@i_vikassharma">
<meta name="twitter:title" content="ReactJs reference notes">
<meta name="twitter:description" content="React reference notes for quick revision #react #frontend">
<meta name="twitter:image" content="https://vikassharma.me/assets/images/react-reference-notes.jpeg">

- [Introduction](#introduction)
- [Components](#components)
    - [Functional Components](#functional-components)
    - [Class Components](#class-components)
- [JSX (JavaScript XML)](#jsx-javascript-xml)
- [Props](#props)
- [State](#state)
- [Hooks](#hooks)
    - [`useState`](#usestate)
    - [`useEffect`](#useEffect)
    - [`useContext`](#useContext)
    - [`useRef`](#useRef)
    - [`Custom Hooks`](#custom-hooks)
- [Rendering](#rendering)
- [Component Communication](#component-communication)
- [Styling](#styling)
- [Virtual DOM](#virtual-dom)
- [React Component Lifecycle](#react-component-lifecycle)
    - [Mounting Phase](#mounting-phase)
        - [`constructor()`](#constructor)
        - [`render()`](#render)
        - [`componentDidMount()`](#componentdidmount)
    - [Updating Phase](#updating-phase)
        - [`static getDerivedStateFromProps()`](#static-getderivedstatefromprops)
        - [`shouldComponentUpdate()`](#shouldcomponentupdate)
        - [`render()`](#render-1)
        - [`getSnapshotBeforeUpdate()`](#getsnapshotbeforeupdate)
        - [`componentDidUpdate()`](#componentdidupdate)
    - [Unmounting Phase](#unmounting-phase)
        - [`componentWillUnmount()`](#componentwillunmount)
    - [Error Handling](#error-handling)
        - [`componentDidCatch()`](#componentdidcatch)
    - [Note](#note)
- [Code lab](#code-lab)
- [Useful links](#useful-links)

## Introduction

ReactJs is an open-source javascript library for building User interfaces. It's declarative, efficient and flexible.

## Components

- Components are the building blocks of React applications.
- They are reusable, self-contained, and can be nested within other components.
- Components can either be **functional** or **class-based**.

### Functional Components

Simple javascript functions that return React elements (also the recommended way of writing Components). They don't have state or lifecycle methods, but they can use hooks to add state and side effects.

```jsx
const HelloComponent = (props) => {
	return <h1>Hello {props.name}</h1>;
};
```

### Class Components

They offer more features such as state and lifecycle methods.

```jsx
class CounterComponent extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			message: "Hello",
			count: 0,
		};
	}

	componentDidMount() {
		// runs after the component is mounted on the DOM
		console.log("Component did mount");
	}

	componentWillUnmount() {
		// runs before the component is about to unmount from the DOM
		console.log("Component will unmount");
	}

	handleClick() {
		this.setState({
			count: this.state.count + 1,
		});
	}

	render() {
		return (
			<div>
				<h1>{this.props.name}, current count: {this.state.count}</h1>
				<button onClick={this.handleClick}>Increment</button>
			</div>
		);
	}
}
```

## JSX (JavaScript XML)

- JSX allows you to write HTML-like code in JavaScript.
- It must be compiled into JavaScript using a tool like Babel.

```jsx
const element = <h1>Hello, React!</h1>;
```

## Props

- Props are **Immutable data** passed from **parent to child** components. They're used to configure the behaviour of a component.
- Access using `props` in functional components or `this.props` in class components.

```jsx
function MyComponent(props) {
	return <h1>{props.name}</h1>;
}

const App = () => {
	return <MyComponent name="John Doe" />;
};
```

## State

- State is a private data store that is associated with a React component.
- Manage component-specific data that can change over time.
- Use `useState` hook or `this.state` in class components.

```jsx
class MyComponent extends React.Component {
  state = {
    count: 0,
  };

  handleClick = () => {
    this.setState({
      count: this.state.count + 1,
    });
  };

  render() {
    return (
      <div>
        <h1>{this.state.count}</h1>
        <button onClick={this.handleClick}>Increment</button>
      </div>
    );
  }
}
```

## Hooks

React Hooks are functions that allow you to "hook into" React state and lifecycle features in function components. They provide a way to manage state and side-effects without using class components.
#### useState

- Allows functional components to manage state.
- Takes an initial state value as an argument and returns an array with two elements: the current state value and a function to update it.
- Example:

```jsx
import React, { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

#### useEffect

- Performs side-effects in function components.
- Takes a function that contains the code for side effects and an optional array of dependencies.
- Only runs the function if any of the dependencies have changed.
- Example:

```jsx
import React, { useState, useEffect } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setSeconds(seconds + 1);
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, [seconds]);

  return <p>Seconds: {seconds}</p>;
}
```

#### useContext

- Accesses the context value created by `React.createContext`.
- Allows components to consume context without introducing a component tree nesting.
-  It consists of **two parts**:
	- a **context provider** that provides the data, and a **context consumer** that consumes the data. 
	- The useContext() hook takes a context object as an argument and returns the current value of that context.
- Example:

```jsx
import React, { useContext } from 'react';

const MyContext = React.createContext();

function MyComponent() {
  const contextValue = useContext(MyContext);

  return <p>Context Value: {contextValue}</p>;
}
```

#### useReducer

- Manages complex state logic by using a reducer function.
- Similar to `useState`, but with more control over state updates.
- Example:

```jsx
import React, { useReducer } from 'react';

const initialState = { count: 0 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>Increment</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>Decrement</button>
    </div>
  );
}
```

#### useRef

- Takes an initial value as an argument and returns an object with a current property that points to the current value of the reference.
- Creates a mutable ref object to interact with DOM elements or store mutable values.
- Does not cause re-renders when the ref value changes.
- Example:

```jsx
import React, { useRef } from 'react';

function InputWithFocus() {
  const inputRef = useRef();

  const focusInput = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

#### Custom Hooks

- Allows you to create reusable hooks to encapsulate logic.
- Typically start with the word "use" to indicate that it's a hook.
- Example:

```jsx
import { useState, useEffect } from 'react';

function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const storedValue = localStorage.getItem(key);
    return storedValue ? JSON.parse(storedValue) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}

// Usage
function App() {
  const [name, setName] = useLocalStorage('name', 'Guest');

  return (
    <div>
      <p>Hello, {name}</p>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
    </div>
  );
}
```

## Rendering

- To render a component, we need to use `ReactDOM.render()` method, which takes two arguments: the component to render and the DOM element where to render it.

```jsx
ReactDOM.render(<Hello name="World" />, document.getElementById("root"));
```

- To use a component inside another component, we need to use it as a JSX element with its name as a tag. We can also pass props to it as attributes.
- For example, if we want to use our Hello component inside another component called App, we can write something like this:

```jsx
function App() {
  return (
    <div>
      <Hello name="Alice" />
      <Hello name="Bob" />
      <Hello name="Charlie" />
    </div>
  );
}
```

## Component Communication

- Parent to Child: Pass data via `props`.
- Child to Parent: Callback functions passed as props.

## Styling

- Inline styles: Use `style` attribute.
- CSS Modules, Styled Components, or popular CSS frameworks.

## Virtual DOM

- The Virtual DOM is a lightweight in-memory representation of the actual DOM.
It's used by React to optimize the process of updating the user interface.
- When there's a change in the application's state, React creates a new Virtual DOM tree.
- React then compares this new Virtual DOM tree with the previous one to identify the differences (diffing).
- The differences are used to update the real DOM, but only the parts that changed.
- This minimizes the number of updates and improves performance.

## Reconciliation

### Reconciliation Process:

- React's process of updating the real DOM based on changes in the Virtual DOM is called reconciliation.
- It ensures that the user interface is always in sync with the application's state.

### Keys in Reconciliation:

- Use unique keys for each element in lists to help React identify elements more efficiently.
- Keys assist in minimizing unnecessary updates and re-renders.

## React Component Lifecycle

### Mounting Phase

#### constructor()

- Constructor is called when a component instance is created.
- Initialize state and bind methods in the constructor.

#### render()

- Render method returns the JSX that represents the component's UI.
- It's a pure function that should not modify the component's state.

#### componentDidMount()

- Invoked after the component is rendered.
- Ideal for setting up side effects, such as data fetching or subscribing to events.

### Updating Phase

#### static getDerivedStateFromProps()

- Rarely used, but if necessary, it's used to update state based on props.

#### shouldComponentUpdate()

- Determines whether the component should re-render.
- Return `true` if you want to update, `false` to skip re-rendering.

#### render()

- Re-render the component with updated props or state.

#### getSnapshotBeforeUpdate()

- Allows you to capture some information before the component updates.
- Use it with `componentDidUpdate` to handle interactions with the DOM.

#### componentDidUpdate()

- Invoked after the component updates and the changes are reflected in the DOM.
- Ideal for performing side effects when props or state change.

### Unmounting Phase

#### componentWillUnmount()

- Called before a component is removed from the DOM.
- Perform cleanup tasks such as canceling timers or unsubscribing from data sources.

### Error Handling

#### componentDidCatch()

- Captures errors in the child components during rendering.
- Implement this method to gracefully handle errors and display fallback UI.

### Note:

- React has moved away from some lifecycle methods in favor of hooks like `useEffect`.
- Focus on class component lifecycle for existing codebases and legacy support.


## Code lab
- Created this very simple react app to revise the basics.
- <a href="https://github.com/vikas3045/task-manager" target="_blank">https://github.com/vikas3045/task-manager</a>

## Useful links
- <a href="https://react.dev/reference/react/" target="_blank">https://react.dev/reference/react/</a>
- <a href="https://create-react-app.dev/" target="_blank">https://create-react-app.dev/</a>