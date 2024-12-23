# Axinite
A powerful open-source engine for advanced celestial mechanics.

![axinite-1](https://github.com/user-attachments/assets/bcd7bc7e-627e-44e5-bfc6-d2ddd787a208)
![axinite-9](https://github.com/user-attachments/assets/8e07f586-3eda-439f-ab1c-8875da6b9e5a)


## Overview
**Axinite** is an engine for calculating celestial motion. 
You can use it to design your own solar systems, predict trajectories of rockets, simulate gravitational interactions and more.

Check out the docs [here](https://jewels86.gitbook.io/axinite/axinite/getting-started).
### What is `axtools`?
`axtools` is a library to help abstract and simplify Axinite. With `axtools`, Developers can deploy Axinite powered applications with ease. 
You can find the docs [here](https://jewels86.gitbook.io/axinite/axtools/quickstart).

### Executable
Axinite will soon be coming to executable format! 

Development is still in progress.

## Supporting Axinite
### Contributing
Feel free to open up a [pull request](https://github.com/jewels86/Axinite/pulls) or an [issue](https://github.com/jewels86/Axinite/issues) if there are any changes you'd like introduced to Axinite.
Any help will be appricated!
### Other ways to support
- Giving this repository a star! This really helps me to get Axinite out to other developers.
- Reaching out! I'd love to hear about your thoughts, ideas, and issues.
- Share the project! Tell you physics/tech-inclined friends about the Axinite engine and see what they think.

## Gallery
![axinite-2](https://github.com/user-attachments/assets/2e952d41-5585-484d-bc3b-05c92aeefe2d)
![axinite-3](https://github.com/user-attachments/assets/ba434ce4-79a3-4a04-a7c4-45232d9fa11a)
![axinite-4](https://github.com/user-attachments/assets/af13ee05-f6ef-4d24-8446-39e6544df2ca)
![axinite-5](https://github.com/user-attachments/assets/c16db758-2ad2-47d8-9f1d-190727f9e881)
![axintie-6](https://github.com/user-attachments/assets/9f2b21b8-e90d-4c5b-9cde-027dfb0ee704)
![axinite-7](https://github.com/user-attachments/assets/100bb29e-3972-4170-bee2-98f9e512116c)
![axinite-8](https://github.com/user-attachments/assets/e39cafc8-7670-4a9d-a0c8-c95682641a95)

## Todos
- Create `ax-cli` executable
- ~~Add live mode~~
- ~~Move actools into axinite.tools and add axinite[tools]~~
- Graceful load funciton exiting
- Add a `save` function
- Move `gravitational_force` out of `Body`
- Phase out `astropy`
- Add console updates every 100-1000 timesteps in `axtools.load(jit=True)`