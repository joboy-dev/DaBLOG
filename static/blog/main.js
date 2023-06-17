const home = document.querySelector('.nav-links .blog-links #home')
const about = document.querySelector('.nav-links .blog-links #about')
const myBlogs = document.querySelector('.nav-links .blog-links #myblogs')
const login = document.querySelector('.nav-links div .user-links #login')
const register = document.querySelector('.nav-links div .user-links #register')


home.addEventListener('click', ()=>{
    // if (home.classList.contains('a')) {
    home.classList.add('active')

    about.classList.remove('active')
    myBlogs.classList.remove('active')
    login.classList.remove('active')
    register.classList.remove('active')
    // }
})

about.addEventListener('click', ()=>{
    // if (about.classList.contains('a')) {
    about.classList.add('active');
    console.log("Working!!!");

    home.classList.remove('active')
    myBlogs.classList.remove('active')
    login.classList.remove('active')
    register.classList.remove('active')
    // } 
})

myBlogs.addEventListener('click', ()=>{
    // if (myBlogs.classList.contains('a')) {
    myBlogs.classList.add('active')

    home.classList.remove('active')
    about.classList.remove('active')
    login.classList.remove('active')
    register.classList.remove('active')
    // }
})

login.addEventListener('click', ()=>{
    // if (login.classList.contains('a')) {
    login.classList.add('active')

    home.classList.remove('active')
    about.classList.remove('active')
    myBlogs.classList.remove('active')
    register.classList.remove('active')
    // }
})

register.addEventListener('click', ()=>{
    // if (register.classList.contains('a')) {
    register.classList.add('active')

    home.classList.remove('active')
    about.classList.remove('active')
    myBlogs.classList.remove('active')
    login.classList.remove('active')
    // }
})