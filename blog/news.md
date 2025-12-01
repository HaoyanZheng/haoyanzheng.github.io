---
layout: home
title: "每日关注天下大事。运筹帷幄之中，决胜千里之外。"
permalink: /blog/
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