import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import ReactDOM from "react-dom/client";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useParams,
} from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from 'axios'
import Showdown from "showdown";
import "./github-markdown.css"
import "./highlight/styles/default.css"
import { NavLink } from "react-router-dom";    

function Home() {
  const { file } = useParams();

  //make query against django db
  const [posts, setPosts] = useState([]);

  let request_link = "http://localhost:8000/api/markdown/"
  useEffect(() => {
    axios.get(request_link)
      .then(response => {
        setPosts(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  let converter = new Showdown.Converter();
  let text = posts;
  let html = [];
  for (const [key, value] of Object.entries(posts)) {
    html = html + converter.makeHtml(value.content);
  }

  const css = `.markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }

  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }`

  return(
    <div style={{backgroundColor: "#0d1117"}}>
    <script src="./highlight/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
      <meta name="viewport" content="width=device-width, initial-scale=1"></meta>
      <style>
        {css}
      </style>
      <article className="markdown-body">
        <div dangerouslySetInnerHTML={{ __html: html }} />
      </article>
    </div>
  );
}

function Documentation() {
  const { file } = useParams();

  //make query against django db
  const [posts, setPosts] = useState([]);

  let request_link = "http://localhost:8000/api/markdown/" + file
  useEffect(() => {
    axios.get(request_link)
      .then(response => {
        setPosts(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  let converter = new Showdown.Converter();
  let text = posts;
  let html = [];
  for (const [key, value] of Object.entries(posts)) {
    html = html + converter.makeHtml(value.content);
  }

  const css = `.markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
  }

  @media (max-width: 767px) {
    .markdown-body {
      padding: 15px;
    }
  }`

  return(
    <div style={{backgroundColor: "#0d1117"}}>
    <script src="./highlight/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
      <meta name="viewport" content="width=device-width, initial-scale=1"></meta>
      <style>
        {css}
      </style>
      <article className="markdown-body">
        <div dangerouslySetInnerHTML={{ __html: html }} />
      </article>
    </div>
  );
}

function App() {
  
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={<Home />}
        />
        <Route
          path="/:file"
          element={<Documentation />}
        />
      </Routes>
    </Router>
  );
}

export default App;
