---
layout: page
title: "News"
permalink: /news/
---

<h1>News</h1>

<ul>
  {% for post in site.posts %}
    {% if post.categories contains "FR News" %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        ({{ post.date | date: "%Y-%m-%d" }})
      </li>
    {% endif %}
  {% endfor %}
</ul>
