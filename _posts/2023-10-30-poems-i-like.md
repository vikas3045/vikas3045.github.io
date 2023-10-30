---
layout: post
title:  "Poems I like"
author: Vikas Sharma
date:   2023-10-30 22:02:00 +0530
categories: [poem]
featured: false
show_preview: false
dont_list_on_dashboard: true
---

{% for post in site.posts %}
    {% if post.categories[0] == "poem" and post.title != "Poems I like" %}
        {% include postbox.html %}
    {% endif %}
{% endfor %}