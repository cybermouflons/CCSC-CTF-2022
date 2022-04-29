# Planet TC-39

**Category**: Web

**Author**: koks

## Description

Do you have what it takes to navigate through the wormholes and penetrate Planet TC-39?

<details>
<summary>Reveal Spoiler</summary>

[This has 2 flags, defined in .env]

Solutions:

- For Flag 1: -0, 0 or undefined, undefined or 2 numbers bigger than the allowed limit for numbers
  - `curl -X POST http://localhost:3000/planet-TC39-1`
  - `curl -X POST http://localhost:3000/planet-TC39-1 -d '{"a": -0, "b": 0}' -H 'content-type: application/json'`
- For Part 2:
  - `curl -X POST http://localhost:3000/planet-TC39-2 -d '{"a": -0, "b": 0}' -H 'content-type: application/json'`

Flags:

- Part 1: "CCSC{so_JS_has_an_em0_streak_its_part_of_what_makes_it_s0_r4d}"
- Part 2: "CCSC{s0ometim3s_JS_is_m0re_f4rt_than_science}"
</details>
