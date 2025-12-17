    var count = 0;
    document.querySelector(".myButton").addEventListener("mouseover", function() {
        var messageDiv = document.querySelector(".message");
        messageDiv.innerHTML = `Додали нове повідомлення! ${count}`;
        messageDiv.style.color = "blue";
        count += 1;
    })




    //document.querySelector(".myButton").addEventListener("click", function() {
    //    alert("УРА! Ви почали свою подорож у анонімному світі!");
    //});