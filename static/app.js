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
                            content += `<div style="color:#718096;margin-top:2px;font-size:0.9em;">${formatTextWithLineBreaks(item.desc)}</div>`;
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