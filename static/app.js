document.addEventListener('DOMContentLoaded', () => {
    const lookupButton = document.getElementById("lookupButton");
    const wordInput = document.getElementById("wordInput");
    const wordDetailsDiv = document.getElementById("wordDetails");

    lookupButton.addEventListener("click", async () => {
        wordDetailsDiv.innerHTML = "";
        const word = wordInput.value;
        const response = await fetch(`/translate?text=${encodeURIComponent(word)}`);
        const data = await response.json();

        orderedKeys.forEach(key => {
            if (data.hasOwnProperty(key)) {
                const detailDiv = document.createElement("div");
                detailDiv.style.marginBottom = "10px";
                const keyStrong = document.createElement('strong');
                keyStrong.textContent = `${keyToChinese[key]}: `;
                detailDiv.appendChild(keyStrong);

                if (key === 'eg_sentences') {
                    const ul = document.createElement('ul');
                    data[key].forEach(item => {
                        const li = document.createElement("li");

                        const engSpan = document.createElement('span');
                        engSpan.innerHTML = formatTextWithLineBreaks(item.eng) + '<br>';
                        engSpan.style.fontStyle = 'italic';

                        const chnSpan = document.createElement('span');
                        chnSpan.innerHTML = formatTextWithLineBreaks(item.translation);
                        chnSpan.style.color = '#666';

                        li.appendChild(engSpan);
                        chnSpan.style.marginTop = '4px';
                        li.appendChild(chnSpan);
                        ul.appendChild(li);
                    });
                    detailDiv.appendChild(ul);
                } else if (key === 'etymologies') {
                    const ul = document.createElement('ul');
                    data[key].forEach(item => {
                        if (!item.value && !item.desc) return;

                        const li = document.createElement("li");
                        let content = '';

                        if (item.value) {
                            content += `<div style="font-weight:600;color:#2d3748;">${formatTextWithLineBreaks(item.value)}</div>`;
                        }
                        if (item.desc) {
                            content += formatTextWithLineBreaks(item.desc);
                        }

                        li.innerHTML = content;
                        ul.appendChild(li);
                    });
                    detailDiv.appendChild(ul);
                } else {
                    let content = data[key];
                    if (typeof content === 'string') {
                        content = formatTextWithLineBreaks(content);
                    }
                    if (key === "usphone" || key === "ukphone") {
                        content = wrapWithParentheses(content);
                    }
                    detailDiv.innerHTML += content;
                }
                wordDetailsDiv.appendChild(detailDiv);
            }
        });
    });
});

const keyToChinese = {
    'word': '单词',
    'ukphone': '英音',
    'usphone': '美音',
    'translations': '翻译',
    'word_forms': '词形',
    'etymologies': '词源',
    'eg_sentences': '例句'
};

const orderedKeys = ["word", "ukphone", "usphone", "translations", "word_forms", "etymologies", "eg_sentences"];

function formatTextWithLineBreaks(text) {
    if (typeof text !== 'string') return text;
    return text.replace(/\n/g, "<br>");
}

function wrapWithParentheses(text) {
    return text ? `[${text}]` : text;
}

// 在DOMContentLoaded事件监听器中添加：
document.getElementById('logoIcon').addEventListener('click', async (e) => {
    e.stopPropagation();
    const bubble = document.getElementById('chatBubble');
    
    try {
        const response = await fetch('/ducksay');
        const data = await response.json();
        bubble.textContent = data.message;  // 动态设置内容
        bubble.style.display = 'block';
    } catch (error) {
        console.error('获取鸭子消息失败:', error);
        bubble.textContent = '连接服务器失败';
        bubble.style.display = 'block';
    }
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('#logoIcon')) {
        document.getElementById('chatBubble').style.display = 'none';
    }
});
const clearInputBtn = document.getElementById('clearInput');
const wordInput = document.getElementById('wordInput');

const searchWrapper = document.createElement('div');
searchWrapper.style.position = 'relative';
wordInput.parentNode.insertBefore(searchWrapper, wordInput);
searchWrapper.appendChild(wordInput.parentNode.removeChild(wordInput));

const suggestionsDiv = document.createElement('div');
suggestionsDiv.style.display = 'none';
suggestionsDiv.style.position = 'absolute';
suggestionsDiv.style.width = '100%';
suggestionsDiv.style.background = 'white';
suggestionsDiv.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
suggestionsDiv.style.zIndex = '1000';
searchWrapper.appendChild(suggestionsDiv);

let timeoutId;
wordInput.addEventListener('input', async () => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(async () => {
        const prefix = wordInput.value.trim();
        if (prefix.length < 2) {
            suggestionsDiv.style.display = 'none';
            return;
        }
        
        try {
            const response = await fetch(`/autocomplete?prefix=${encodeURIComponent(prefix)}`);
            const suggestions = await response.json();
            
            suggestionsDiv.innerHTML = suggestions.map(word => `
                <div style="padding: 8px; cursor: pointer; border-bottom: 1px solid #eee; 
                    &:hover { background: #f8f9fa; }">
                    ${word}
                </div>
            `).join('');
            
            suggestionsDiv.style.display = suggestions.length ? 'block' : 'none';
            
            suggestionsDiv.querySelectorAll('div').forEach(div => {
                div.addEventListener('click', () => {
                    wordInput.value = div.textContent.trim(); 
                    suggestionsDiv.style.display = 'none';
                    lookupButton.click();
                });
            });
        } catch (error) {
            console.error('Autocomplete error:', error);
        }
    }, 300);
});

// 修改后的回车键监听
wordInput.addEventListener('keydown', (e) => {
    if (e.keyCode === 13) { // Enter key
        e.preventDefault();
        clearTimeout(timeoutId);  // 新增：清除自动完成定时器
        suggestionsDiv.style.display = 'none';
        lookupButton.click();
    }
});

document.addEventListener('click', (e) => {
    if (!searchWrapper.contains(e.target)) {
        suggestionsDiv.style.display = 'none';
    }
});

clearInputBtn.addEventListener('click', () => {
    wordInput.value = '';
    clearInputBtn.style.display = 'none';
    wordDetailsDiv.innerHTML = '';
});