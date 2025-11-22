---
layout: home
title: "Blog"
permalink: /blog/
---

这里是我的每日法语新闻 + 笔记。

<ul>
{% for post in site.posts %}
  <li>
    <a href="{{ post.url | relative_url }}">
      {{ post.date | date: "%Y-%m-%d" }} - {{ post.title }}
    </a>
  </li>
{% endfor %}
</ul>
