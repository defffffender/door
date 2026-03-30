/* ============================================================
   Chat Widget — Scripted bot for Door Company
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {
    const widget = document.getElementById('chatWidget');
    const btn = document.getElementById('chatWidgetBtn');
    const closeBtn = document.getElementById('chatCloseBtn');
    const messagesEl = document.getElementById('chatMessages');
    const inputArea = document.getElementById('chatInputArea');

    if (!widget || !btn) return;

    /* --- State --- */
    let state = 'idle';     // idle | waiting_input | done
    let flow = null;         // callback | consult | product | proposal
    let step = 0;
    let data = {};

    /* --- Open / Close --- */
    let opened = false;

    function openChat() {
        widget.classList.add('open');
        if (!opened) { opened = true; startChat(); }
    }

    btn.addEventListener('click', function () {
        if (widget.classList.contains('open')) {
            widget.classList.remove('open');
        } else {
            openChat();
        }
    });

    closeBtn.addEventListener('click', function () {
        widget.classList.remove('open');
        localStorage.setItem('chatWidgetShown', '1');
    });

    /* --- Auto-open on first visit (per browser session) --- */
    if (!sessionStorage.getItem('chatAutoOpened')) {
        setTimeout(function () {
            if (!widget.classList.contains('open')) {
                openChat();
                sessionStorage.setItem('chatAutoOpened', '1');
            }
        }, 5000);
    }

    /* --- Helpers --- */
    function scrollDown() {
        setTimeout(function () { messagesEl.scrollTop = messagesEl.scrollHeight; }, 50);
    }

    function addMsg(text, who) {
        var icon = who === 'bot' ? 'fa-robot' : 'fa-user';
        var div = document.createElement('div');
        div.className = 'chat-msg chat-msg--' + who;
        div.innerHTML =
            '<div class="chat-msg__avatar"><i class="fas ' + icon + '"></i></div>' +
            '<div class="chat-msg__bubble">' + text + '</div>';
        messagesEl.appendChild(div);
        scrollDown();
    }

    function showTyping() {
        var div = document.createElement('div');
        div.className = 'chat-msg chat-msg--bot';
        div.id = 'chatTyping';
        div.innerHTML =
            '<div class="chat-msg__avatar"><i class="fas fa-robot"></i></div>' +
            '<div class="chat-msg__bubble"><div class="chat-typing"><span></span><span></span><span></span></div></div>';
        messagesEl.appendChild(div);
        scrollDown();
    }

    function removeTyping() {
        var t = document.getElementById('chatTyping');
        if (t) t.remove();
    }

    function botSay(text, cb) {
        showTyping();
        setTimeout(function () {
            removeTyping();
            addMsg(text, 'bot');
            if (cb) cb();
        }, 800);
    }

    function showOptions(opts) {
        inputArea.innerHTML = '';
        var wrap = document.createElement('div');
        wrap.className = 'chat-options';
        opts.forEach(function (o) {
            var b = document.createElement('button');
            b.className = 'chat-opt-btn';
            b.textContent = o.label;
            b.addEventListener('click', function () {
                addMsg(o.label, 'user');
                inputArea.innerHTML = '';
                o.action();
            });
            wrap.appendChild(b);
        });
        inputArea.appendChild(wrap);
        scrollDown();
    }

    function showInput(placeholder, onSubmit) {
        inputArea.innerHTML = '';
        var row = document.createElement('div');
        row.className = 'chat-input-row';
        var inp = document.createElement('input');
        inp.className = 'chat-input';
        inp.type = 'text';
        inp.placeholder = placeholder;
        var sendBtn = document.createElement('button');
        sendBtn.className = 'chat-send';
        sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';

        function submit() {
            var val = inp.value.trim();
            if (!val) return;
            addMsg(val, 'user');
            inputArea.innerHTML = '';
            onSubmit(val);
        }

        sendBtn.addEventListener('click', submit);
        inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') submit(); });

        row.appendChild(inp);
        row.appendChild(sendBtn);
        inputArea.appendChild(row);
        inp.focus();
    }

    function clearInput() { inputArea.innerHTML = ''; }

    /* --- CSRF --- */
    function getCsrf() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) return meta.content;
        var inp = document.querySelector('[name=csrfmiddlewaretoken]');
        return inp ? inp.value : '';
    }

    /* --- Submit to backend --- */
    function submitData() {
        fetch('/contacts/chat/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf()
            },
            body: JSON.stringify(data)
        }).catch(function () {});
    }

    /* --- Flow: Ask name then phone, then done --- */
    function askName(thankMsg) {
        botSay('Как Вас зовут?', function () {
            showInput('Ваше имя', function (name) {
                data.name = name;
                askPhone(thankMsg);
            });
        });
    }

    function askPhone(thankMsg) {
        botSay('Ваш номер телефона?', function () {
            showInput('+998 ...', function (phone) {
                data.phone = phone;
                submitData();
                botSay(thankMsg, function () { showRestart(); });
            });
        });
    }

    /* --- Restart option --- */
    function showRestart() {
        showOptions([
            { label: 'Начать заново', action: function () { data = {}; startChat(); } }
        ]);
    }

    /* --- Start --- */
    function startChat() {
        messagesEl.innerHTML = '';
        clearInput();
        data = {};
        flow = null;

        botSay('Добро пожаловать! Что Вас интересует?', function () {
            showOptions([
                {
                    label: 'Оставить заявку на звонок',
                    action: function () { flow = 'callback'; flowCallback(); }
                },
                {
                    label: 'Получить консультацию',
                    action: function () { flow = 'consult'; flowConsult(); }
                },
                {
                    label: 'Узнать о продукции',
                    action: function () { flow = 'product'; flowProduct(); }
                },
                {
                    label: 'Есть предложение',
                    action: function () { flow = 'proposal'; flowProposal(); }
                }
            ]);
        });
    }

    /* --- Flow 1: Callback --- */
    function flowCallback() {
        data.message = '[Заявка на звонок]';
        askName('Спасибо! Мы перезвоним Вам в ближайшее время.');
    }

    /* --- Flow 2: Consultation --- */
    function flowConsult() {
        botSay('Опишите Ваш вопрос', function () {
            showInput('Ваш вопрос...', function (msg) {
                data.message = '[Консультация] ' + msg;
                askName('Спасибо! Наш специалист свяжется с Вами.');
            });
        });
    }

    /* --- Flow 3: Product info --- */
    function flowProduct() {
        botSay('Вы можете посмотреть наш каталог:', function () {
            addMsg('<a href="/catalog/" class="chat-link-btn"><i class="fas fa-door-open"></i> Открыть каталог</a>', 'bot');
            botSay('Или оставьте заявку и мы проконсультируем', function () {
                showOptions([
                    {
                        label: 'Оставить заявку',
                        action: function () {
                            data.message = '[Интерес к продукции]';
                            askName('Спасибо! Мы свяжемся с Вами для консультации.');
                        }
                    },
                    {
                        label: 'Спасибо, посмотрю каталог',
                        action: function () {
                            botSay('Хорошо! Если возникнут вопросы — пишите.', function () { showRestart(); });
                        }
                    }
                ]);
            });
        });
    }

    /* --- Flow 4: Proposal --- */
    function flowProposal() {
        botSay('Опишите Ваше предложение', function () {
            showInput('Ваше предложение...', function (msg) {
                data.message = '[Предложение] ' + msg;
                askName('Спасибо! Мы рассмотрим Ваше предложение.');
            });
        });
    }
});
