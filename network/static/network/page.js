console.log("Hello World");
document.addEventListener('DOMContentLoaded', function(){
    const likeButtons = document.getElementsByClassName('like_button');
    const likeBtns = document.querySelectorAll(".like_button")
    const editButtons = document.getElementsByClassName('edit_post')
    const likeCount = document.getElementsByClassName("like_count")
    const follow = document.getElementById("follow")
    const user = document.getElementById("user_cred")
    const seeFollowing = document.getElementById("show-following")
    const seeFollowers = document.getElementById("show-followers")
    // console.log(likeButtons.innerHTML)
    // console.log(`test ${user.innerHTML}`)

    likeBtns.forEach(button => {
        button.addEventListener('click', () =>{
            const postElement = button.closest('.buzz-body')
            const postId = postElement.getAttribute('data-post-id')
            const likeCountElement = postElement.querySelector('.like_count')
            const likeCount = parseInt(likeCountElement.textContent, 10)
            console.log(likeCount)
            
            // postElement.children.
            
            console.log(likeCountElement)
            console.log(postElement)

            const requestOption = {
                method:"POST",
                header: "application/json"
            }

            fetch(`/like/${postId}`,{
                method: "GET"
            })
            .then(response => response.json())
            .then(post => {
                if(post.liked == false){
                    likeCountElement.innerHTML = likeCount -1
                    button.innerHTML  = "Like"
                }else{
                    likeCountElement.innerHTML = likeCount +1
                    button.innerHTML = "Dislike"
                }
            })

        })
    })

    // for (var i = 0; i<likeButtons.length; i++){
    //     let id = i 
    //     let activeButton = likeButtons[i]
    //     console.log(activeButton)
    //     let activeLikeCount = likeCount[i]
    //     console.log(activeLikeCount)
    //     activeButton.addEventListener('click', () => likehandler(id, activeButton=activeButton, activeLikeCount=activeLikeCount));
    // }
    
    for( var i = 0; i<editButtons.length; i++){
        let id = i 
        let activeEditButton = editButtons[i]
        activeEditButton.addEventListener('click', () => editHandler(id , activeEditButton = activeEditButton))
    }
    follow.addEventListener('click', () => reloadPage("follow",followUser(user.innerHTML)))
    seeFollowing.addEventListener('click', () => showFollowModal("following-modal"))
    seeFollowers.addEventListener('click', () => showFollowModal("followers-modal"))
    // document.querySelector(".edit_post").addEventListener("click", editPost(id))x
    likehandler()
});

function editHandler(id, activeEditButton){
    const buzzId = id
    console.log(`This is the buzz id ${buzzId}`)
    const container = activeEditButton.parentNode
    const editbuttonParent = container.parentElement


    const editPanels = document.getElementsByClassName('editPanels')
    let panel = null

    for (var i = 0; i<editPanels.length; i++){
        panel = editPanels[i]
        
        if (i == buzzId){

            editPanels[i].classList.remove("hidePanels")
            editbuttonParent.style.setProperty("display", "grid","important");
            container.classList.add('hidePanels')
            console.log(panel)
        }else{ 

            editPanels[i].classList.add("hidePanels")
            editbuttonParent.style.display = 'block'
            
        }
        console.log(`This is the buzz id ${buzzId} and panel id ${i}`)

    }
};

// function followUser(){
//     console.log("follow user button clicked")
// }
function followUser(user){
    console.log(`${user} is to follow`)
    fetch(`follow/${user}`)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        let followButton = document.getElementById("follow")
        let followersCount = document.getElementById("followers-count")
        let followerCountInt = parseInt(followersCount.innerHTML)
        if(data.following == "True"){
            followButton.innerHTML = "Unfollow"
            followersCount.innerHTML = followerCountInt + 1
        }else{
            followButton.innerHTML = "Follow"
            followersCount.innerHTML = followerCountInt - 1
        }
    })
}

function likehandler(id, activeButton, activeLikeCount){
    console.log('button element clicked')
    console.log(`button ${id+1}`)
    let object = id + 1
    console.log(`The active like count ${activeLikeCount.innerHTML}`)
    const requestOption = {
        method: "POST",
        header: "application/json"
        };
    fetch(`like/${object}`, {
        method: "GET",
    })
    .then(response => response.json())
    .then(post => {
        // likeCount.innerHTML = `likes:${liked}`;
        console.log(post)
        if(post.liked == false){
            
            console.log(`Is this post liked ${post.liked} was false`)
            console.log("liked")
            i = parseInt(activeLikeCount.innerHTML) + 1
            console.log(`Int version${ i } `)
            activeLikeCount.innerHTML = i
            activeButton.innerHTML = "Liked Now Dislike";
            const splitData = post.data.split(/[|]|{|}/)
            const likerData = splitData[2]
            const splitDataDict = likerData.split(":")
            console.log(splitDataDict)
            const splitLikerData = splitDataDict[1]
            console.log(splitLikerData.split(/,/).length)
            const countLike = splitLikerData.split(/,/).length
            like_count.innerHTML = `${countLike + " like(s)"}`
            // like_count.innerHTML = Object.keys(post.data[0])
            // console.log(like_count)
            // console.log(...post.data)

        }else{

            
            console.log(`Is this post liked ${post.liked}`)
            console.log("liked")
            like_count = activeButton.nextElementSibling
            console.log(` number of likes: ${like_count}`)
            i = parseInt(activeLikeCount.innerHTML) - 1
            console.log(`Int version${ i-1 } `)
            activeLikeCount.innerHTML = i
            activeButton.innerHTML = "Disliked now Like";
            const splitData = post.data.split(/[|]|{|}/)
            console.log(splitData[2])
            const likerData = splitData[2]
            const splitDataDict = likerData.split(":")
            console.log(splitDataDict)
            const splitLikerData = splitDataDict[1]
            console.log(typeof splitLikerData)
            console.log(splitLikerData.length)
            console.log(splitLikerData.split(/,/).length)
            // const countLike = splitLikerData.split(/,/).length
            // like_count.innerHTML = `${countLike + " like(s)"}`

            console.log(post.data.split(/[|]|{|}/))
            console.log(post.data.split("{").splice(0, 1));
            const newData = post.data.splice(-1, 1);
            console.log(newData)
            
            console.log(like_count)
            console.log(...post.data)
            console.log(newData)

        }
    } )

}

function save_edit(id){
    
    fetch(`save_edit/${id}`, {

        method: "PUT",
        body: JSON.stringify({
            body: document.querySelector()
        })
    })
    .then(response)
}

function showFollowModal(modalId){
    let el = document.getElementById(modalId)
    console.log(el)
    if(el.style.display === "none"){
        el.style.display = "flex"
        el.style.zIndex = 1
        document.body.style.overflow = "hidden"
    }else{
        el.style.display = "none"
        el.style.zIndex = 0
        document.body.style.overflow = "scroll"
    }
}

// async function reloadPage(modalId){
//     () => window.location.reload()
//     console.log("asyn function running")
//     console.log(modalId)
//     return modalId
// }

// reloadPage(modalId)
// .then(function(value){ showFollowModal(value) }
// )

// async function reloadPage(modalId){
//     () => window.location.reload()
//     let myPromise = new Promise((resolve) => {
//         resolve(modalId)
//     });
//     showFollowModal(await myPromise)
// }

async function reloadPage(modalId, callBack){
    window.location.reload()
    window.onload = callBack(modalId)
}

