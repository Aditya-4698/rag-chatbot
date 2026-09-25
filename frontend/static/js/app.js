/* API CONFIGURATION */

const API_BASE = "/api";


/* DOM ELEMENTS */

const authSection =
    document.getElementById("authSection");

const dashboardSection =
    document.getElementById("dashboardSection");

const loginForm =
    document.getElementById("loginForm");

const registerForm =
    document.getElementById("registerForm");

const loginBtn =
    document.getElementById("loginBtn");

const registerBtn =
    document.getElementById("registerBtn");

const showRegisterBtn =
    document.getElementById("showRegisterBtn");

const showLoginBtn =
    document.getElementById("showLoginBtn");

const authMessage =
    document.getElementById("authMessage");

const usernameDisplay =
    document.getElementById("usernameDisplay");

const documentsList = document.getElementById(
    "documentsList"
);

const uploadBtn = document.getElementById(
    "uploadBtn"
);

const fileInput = document.getElementById(
    "fileInput"
);

const sendBtn = document.getElementById(
    "sendBtn"
);

const questionInput = document.getElementById(
    "questionInput"
);

const chatMessages = document.getElementById(
    "chatMessages"
);

const chatStatus = document.getElementById(
    "chatStatus"
);

const logoutBtn = document.getElementById(
    "logoutBtn"
);


/*  AUTHENTICATION */

function getToken() {
    return localStorage.getItem("authToken")
}

function authHeaders() {
    return {
        "Authorization": `Token ${getToken()}`
    };
}

/* Show Register form */

showRegisterBtn.addEventListener(
    "click", () => {

        loginForm.classList.add(
            "hidden"
        );

        registerForm.classList.remove(
            "hidden"
        );

        authMessage.textContent = "";
    }
);


/* Show Login */

showLoginBtn.addEventListener(
    "click", () => {
        registerForm.classList.add(
            "hidden"
        );

        loginForm.classList.remove(
            "hidden"
        );

        authMessage.textContent = "";
    }
);

/* Register */

registerBtn.addEventListener(
    "click", registerUser
);

async function registerUser() {
    const username = document.getElementById(
        "registerUsername"
    ).value.trim();

    const email = document.getElementById(
        "registerEmail"
    ).value.trim();

    const password = document.getElementById(
        "registerPassword"
    ).value.trim();

    /* check field */

    if (!username || !email || !password) {
        authMessage.textContent =
            "All fields are required.";
        return;
    }

    authMessage.textContent = "Creating account...";

    try {

        const response = await fetch(
            `${API_BASE}/auth/register/`,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        /*registration error */

        if (!response.ok) {

            authMessage.textContent = JSON.stringify(data);
            return;
        }

        /* save token */

        localStorage.setItem(
            "authToken",
            data.token
        );

        showDashboard();

    } catch (error) {
        console.error(error);

        authMessage.textContent =
            "Unable to connect to server."

    }
}

/*LOgin */

loginBtn.addEventListener(
    "click", loginUser
);


async function loginUser() {

    const username = document.getElementById(
        "loginUsername"
    ).value.trim();

    const password = document.getElementById(
        "loginPassword"
    ).value;

    /* check filed */

    if (!username || !password) {

        authMessage.textContent =
            "Username and Password are required.";

        return;
    }

    authMessage.textContent =
        "Logging in...";

    try {

        const response = await fetch(
            `${API_BASE}/auth/login/`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        const data = await response.json();

        /*login error */

        if (!response.ok) {

            authMessage.textContent =
                data.detail ||
                "Invalid username or password.";

            return;
        }

        localStorage.setItem(
            "authToken",
            data.token
        );

        showDashboard();

    } catch (error) {
        console.error(error);

        authMessage.textContent =
            "Unable to connect to server.";

    }
}

document.getElementById("loginUsername").addEventListener(
    "keydown",
    event => {
        if (event.key === "Enter") {
            loginUser();
        }
    }
);

document.getElementById("loginPassword").addEventListener(
    "keydown",
    event => {
        if (event.key === "Enter") {
            loginUser();
        }
    }
);


/*Show Dashboard */

async function showDashboard() {
    authSection.classList.add(
        "hidden"
    );

    dashboardSection.classList.remove(
        "hidden"
    );

    await loadCurrentUser();
    await loadDocuments();
    await loadChatHistory();
}

/* load current user */

async function loadCurrentUser() {

    try {
        const response = await fetch(
            `${API_BASE}/auth/me/`,
            {
                headers: authHeaders()
            }
        );

        if (!response.ok) {
            logoutLocal();
            return;
        }

        const user = await response.json();

        usernameDisplay.textContent =
            `Radhey Radhey, ${user.username}`;
    } catch (error) {
        console.error(error);

        logoutLocal();

    }
}


/* Load Documents */

async function loadDocuments() {

    const response = await fetch(
        `${API_BASE}/documents/`,
        {
            headers: authHeaders()
        }
    );

    if (!response.ok) {
        console.error("Failed to load documents.");
        return;
    }

    const documents = await response.json();

    renderDocuments(documents);
}


/*  RENDER DOCUMENTS */

function renderDocuments(documents) {

    documentsList.innerHTML = "";

    if (documents.length === 0) {

        documentsList.innerHTML = `
            <p class="empty-state">
                No documents yet.
            </p>
        `;

        return;
    }

    documents.forEach(doc => {

        const card = document.createElement("div");

        card.className = "document-card";

        card.innerHTML = `
            <div class="document-title">
                📄 ${escapeHTML(doc.title)}
            </div>

            <div class="document-info">
                ${doc.chunk_count} chunks
            </div>

            <span class="status ${doc.status}">
                ${doc.status}
            </span>

            <button
                class="delete-document-btn"
                data-id="${doc.id}"
            >
                Delete
            </button>
        `;

        documentsList.appendChild(card);
    });

    document.querySelectorAll(".delete-document-btn")
        .forEach(button => {

            button.addEventListener(
                "click", () => deleteDocument(
                    button.dataset.id
                )
            );
        });
}


/* Escape HTML */

function escapeHTML(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


/* Delete DOCument */

async function deleteDocument(documentId) {

    const confirmed =
        confirm("Are you sure you want to delete this documents?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_BASE}/documents/${documentId}/`,
            {
                method: "DELETE",
                headers: authHeaders()
            }
        );

        if (!response.ok) {
            alert(
                "Unable to delete document."
            );
            return;
        }

        await loadDocuments();
    } catch (error) {
        console.error(error);

        alert("Something went wrong.");
    }
}

/* Upload Button */

uploadBtn.addEventListener(
    "click",
    () => {
        fileInput.click();
    }
);


/* File Input */

fileInput.addEventListener(
    "change",
    uploadDocument
);


/* Upload Document */

async function uploadDocument() {

    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Only PDF file supported.");
        return;
    }

    /* form data */


    const formData = new FormData();

    formData.append("title", file.name);

    formData.append("file", file);

    uploadBtn.disabled = true;

    /* status */

    chatStatus.textContent = "Uploading and processing PDF...";

    /* API request */

    try {

        const response = await fetch(
            `${API_BASE}/documents/`,
            {
                method: "POST",
                headers: authHeaders(),
                body: formData
            }
        );

        if (!response.ok) {
            alert("Document upload failed.");

            chatStatus.textContent = "Upload failed.";

            return;
        }

        await response.json();

        fileInput.value = "";

        chatStatus.textContent = "Document ready";

        await loadDocuments();
    } catch (error) {
        console.error(error);

        chatStatus.textContent = "Upload failed.";

    } finally {
        uploadBtn.disabled = false;
    }
}


/*  SEND BUTTON */

sendBtn.addEventListener(
    "click", sendQuestion
);


/*  SEND QUESTION */

async function sendQuestion() {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addUserMessage(question);

    questionInput.value = "";

    chatStatus.textContent = "Thinking....";

    sendBtn.disabled = true;

    try {

        const response = await fetch(
            `${API_BASE}/chat/`,
            {
                method: "POST",
                headers: {
                    ...authHeaders(),
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        removeTypingIndicator();

        /* Error response */

        if (!response.ok) {

            let errorMessage =
                "Unable to get an answer";

            try {

                const error =
                    await response.json();

                errorMessage = error.detail || errorMessage;
            } catch (error) {
                console.error(error);

            }

            addAIMessage(
                errorMessage
            );

            return;
        }

        const data = await response.json();

        // console.log("CHAT RESPONSE:", data);

        /* Show AI answer */

        addAIMessage(
            data.answer,
            data.sources
        );
    } catch (error) {
        console.error(error);

        removeTypingIndicator();

        addAIMessage(
            "Connection issue from server."
        );

    } finally {
        sendBtn.disabled = false;

        chatStatus.textContent = "Ready";
    }
}

/* ADD USER MESSAGE */

function addUserMessage(message) {

    const div = document.createElement("div");

    div.className = "message user-message";

    div.textContent = message;

    chatMessages.appendChild(div);

    scrollChat();
}

/*Add User message */

function addUserMessage(
    message,
    shouldScroll = true
) {

    const div = document.createElement("div");

    div.className = "message user-message";

    div.textContent = message;

    chatMessages.appendChild(div);

    if (shouldScroll) {
        scrollChat();
    }
}

/*  ADD AI MESSAGE */

function addAIMessage(
    answer,
    sources = [],
    shouldScroll = true
) {
    const div = document.createElement("div");

    div.className = "message bot-message";

    let sourcesHTML = "";

    if (sources.length > 0) {

        sourcesHTML = `
        <div class = "sources">
            <strong>Sources: </strong>
                <ul>
                    ${sources.map(source => `
                        <li>
                            📄 Document #${source.document_id}
                            — Page ${source.page ?? "N/A"}
                            — Chunk ${source.chunk_index ?? "N/A"}
                        </li>
                        `).join("")}
                </ul>
        </div>
        `;
    }

    div.innerHTML = `
        <div class="answer-content">
            ${escapeHTML(answer)}
        </div>

        ${sourcesHTML}
    `;

    chatMessages.appendChild(div);

    if(shouldScroll){
        scrollChat();
    }
}

/* SCROLL CHAT */

function scrollChat() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* chat history */

async function loadChatHistory(){

    try{

        const response = await fetch(
            `${API_BASE}/chat/history/`,
            {
                headers: authHeaders()
            }
        );
        
        if(!response.ok){
            return;
        }

        const history = await response.json();

        renderChatHistory(history);

    } catch(error) {
        console.error("Chat history error",error);
        
    }
}

/* Render chat history */

function renderChatHistory(history){

    chatMessages.innerHTML = "";

    if(history.length === 0){

        chatMessages.innerHTML = `
            <div class = "welcome-message">
                <h3>👋 Welcome</h3>
                
                <p>
                    Upload  a PDF and ask questions about your document.
                </p>
            
            </div>
        `;
        return;
    }

    /* Reverse history */

    const orderedHistory = 
        [...history].reverse();

    orderedHistory.forEach(message => {

        addUserMessage(
            message.question,
            false
        );

        addAIMessage(
            message.answer,
            [],
            false
        );
    });

    scrollChat();
}

/* Typing Indicator */

function showTypingIndicator(){

    const div = document.createElement("div");

    div.id = "typingIndicator";

    div.className = "message bot-message";

    div.innerHTML =`
        <span>
            AI is thinking....
        </span>
    `;

    chatMessages.appendChild(div);

    scrollChat();
}

/* Remove typingg indicator */

function removeTypingIndicator(){

    const indicator = 
        document.getElementById("typingIndicator");

    if(indicator){
        indicator.remove();
    }
}

/* Enter send button */

questionInput.addEventListener(
    "keydown", event => {

        if ( event.key === "Enter" && !event.shiftKey){

            event.preventDefault();

            sendQuestion();
        }
    }
);

/* LOGOUT */

logoutBtn.addEventListener(
    "click",
    async () => {

        try {
            await fetch(
                `${API_BASE}/auth/logout/`,
                {
                    method: "POST",
                    headers: authHeaders()
                }
            );
        } catch (error) {
            console.error(error);

        }

        localStorage.removeItem(
            "authToken"
        );

        window.location.href = "/";
    }
);

/* local logout */

function logoutLocal(){

    localStorage.removeItem(
        "authToken"
    );

    authSection.classList.remove(
        "hidden"
    );

    dashboardSection.classList.add(
        "hidden"
    );
}


/* PAGE INITIALIZATION */

async function initialization() {

    const token = getToken();

    if (!token) {

        authSection.classList.remove(
            "hidden"
        );

        dashboardSection.classList.add(
            "hidden"
        );

        return;

    }
    
    try {
        const response = await fetch(
            `${API_BASE}/auth/me/`,
            {
                headers: authHeaders()
            }
        );

        if (!response.ok) {
            logoutLocal();
            return;
        }

        authSection.classList.add(
            "hidden"
        );

        dashboardSection.classList.remove(
            "hidden"
        );

        const user = await response.json();

        usernameDisplay.textContent = `Radhey Radhey, ${user.username}`;

        await loadDocuments();

        await loadChatHistory();

    } catch(error) {
        console.error(
            "Initialization error",error
        );
        
    }
}

/* Start Application */

initialization();