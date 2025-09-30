
function toggleAnswer(id){
    const div = document.getElementById('answer-' + id);
    const btn = document.getElementById('answer-btn-' + id);
    const isHidden = (div.style.display === 'none' || div.style.display === '');
    div.style.display = isHidden ? 'block' : 'none';
    btn.innerText = isHidden ? '답 숨기기' : '답 보기';
}

function toggleExplanation(id){
    const div = document.getElementById('explanation-' + id);
    const btn = document.getElementById('toggle-btn-' + id);
    const isHidden = (div.style.display === 'none' || div.style.display === '');
    div.style.display = isHidden ? 'block' : 'none';
    btn.innerText = isHidden ? '해설 숨기기' : '해설 보기';
}

function editExplanation(id){
    const explanationDiv = document.getElementById('explanation-' + id);
    const editContainer = document.getElementById('edit-container-' + id);
    const current = explanationDiv.textContent; 

    editContainer.innerHTML = `<textarea id='edit-area-${id}'>${current}</textarea>
                               <button class='btn' onclick='saveExplanation(${id})'>저장</button>`;
    editContainer.style.display = 'block';
    explanationDiv.style.display = 'none';
}

async function saveExplanation(id){
    const newText = document.getElementById('edit-area-' + id).value;
    const res = await fetch(`/update/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ explanation: newText })
    });
    if(res.ok){
        const explanationDiv = document.getElementById('explanation-' + id);
        const editContainer = document.getElementById('edit-container-' + id);
        explanationDiv.innerHTML = newText.replace(/\n/g, "<br>");
        explanationDiv.style.display = 'block';
        editContainer.style.display = 'none';
    } else {
        alert("저장 실패");
    }
}
