![CCSC CTF 2021](_assets/banner.png)
# CCSC-CTF-2022

## Repository Structure

This is the official repository with the challenges published in CCSC CTF 2022. Each challenge has a `public` and `setup` folder (if applicable) and is accompanied with a short description. The `setup` folder contains all the files required to build and host the challenge and usually contains the flag and a proof of concept solution as well. Alternatively, the `public` folder contains the files that are released to the participant during the competition.

## Dependencies

Although some of the challenges may run as is, it is recommended that you have **docker** and **docker-compose** installed and use the provided scripts to run the challenges to ensure isolation and therefore proper environment setup.

For a more detailed description of the folder structure for challenges, please see the [Jeopardy Creation Guide](https://www.notion.so/Jeopardy-CTF-Challenge-Creation-770b62e8556442a3826cb6593d6affa4) on the Cybermouflons wiki.

## Reserved Ports

Port 8000 will be used for serving static artifacts

## Challenges

### Misc

| Name                            | Author | Ports |
| ------------------------------- | ------ | ----- |
| [Pickle Rick](misc/pickle-rick) | rok0s  | -     |

### Stego

| Name                               | Author | Ports |
| ---------------------------------- | ------ | ----- |
| [UFO](stego/ufo)                   | koks   | -     |
| [Meeting Area](stego/meeting-area) | koks   | -     |

### Web

| Name                                     | Author | Ports |
| ---------------------------------------- | ------ | ----- |
| [Planet-TC39](web/planet-tc39)           | koks   | 3000  |
| [Morty's Cleanup List](web/morty's-list) | s1kk1s | 5000  |
### Pwn

| Name                                               | Author  | Ports |
| -------------------------------------------------- | ------- | ----- |
| [Custom_heap_allocator](pwn/custom_heap_allocator) | condiom | 1337  |
| [automated_pwn](pwn/automated_pwn)                 | condiom | 1338  |