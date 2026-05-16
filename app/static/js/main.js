document.addEventListener('DOMContentLoaded', function () {
    // === THEME TOGGLE ===
    const themeToggleBtn = document.getElementById('theme-toggle');
    const darkIcon = document.getElementById('theme-toggle-dark-icon');
    const lightIcon = document.getElementById('theme-toggle-light-icon');

    const updateIcons = () => {
        if (document.documentElement.classList.contains('dark')) {
            lightIcon.classList.remove('hidden');
            darkIcon.classList.add('hidden');
        } else {
            darkIcon.classList.remove('hidden');
            lightIcon.classList.add('hidden');
        }
    };

    if (themeToggleBtn && darkIcon && lightIcon) {
        updateIcons();
        themeToggleBtn.addEventListener('click', function () {
            document.documentElement.classList.toggle('dark');
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('color-theme', isDark ? 'dark' : 'light');
            updateIcons();
        });
    }

    // === HISTORY & DISPLAY UTILS ===
    const updateHistory = (category, formula, result) => {
        let history = JSON.parse(localStorage.getItem('calc_history') || '[]');
        history.unshift({ category, formula, result, timestamp: new Date().toLocaleString() });
        history = history.slice(0, 10); // Keep last 10
        localStorage.setItem('calc_history', JSON.stringify(history));
        renderHistory();
    };

    const renderHistory = () => {
        const fullContainer = document.getElementById('full-history-list');
        const history = JSON.parse(localStorage.getItem('calc_history') || '[]');
        
        if (fullContainer) {
            if (history.length === 0) {
                fullContainer.innerHTML = `
                    <div class="text-center py-20 bg-white dark:bg-slate-800 rounded-3xl border border-dashed border-slate-200 dark:border-slate-700">
                        <p class="text-slate-400">Belum ada riwayat perhitungan.</p>
                    </div>
                `;
                return;
            }
            fullContainer.innerHTML = history.map(item => `
                <div class="p-6 bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 flex justify-between items-center">
                    <div>
                        <div class="flex items-center space-x-2 mb-1">
                            <span class="px-2 py-0.5 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-[10px] font-bold uppercase rounded-md">${item.category}</span>
                            <span class="text-xs text-slate-400">${item.timestamp}</span>
                        </div>
                        <div class="font-mono text-lg font-bold text-slate-700 dark:text-slate-200">${item.formula}</div>
                    </div>
                    <div class="text-2xl font-black text-blue-600 dark:text-blue-400">
                        = ${Array.isArray(item.result) ? item.result[0] + '...' : item.result}
                    </div>
                </div>
            `).join('');
        }
    };

    const clearHistoryBtn = document.getElementById('clear-history');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', () => {
            if (confirm('Apakah Anda yakin ingin menghapus semua riwayat?')) {
                localStorage.removeItem('calc_history');
                renderHistory();
            }
        });
    }

    const showResult = (id, containerId, data, category) => {
        const el = document.getElementById(id);
        const container = document.getElementById(containerId);
        if (!el || !container) return;

        // Render result, formula, and steps
        let html = `
            <div class="mb-4">
                <p class="text-xs font-bold text-slate-400 uppercase mb-1">Rumus</p>
                <div class="font-mono text-lg text-blue-600 dark:text-blue-400 font-bold">${data.formula}</div>
            </div>
            <div class="mb-4">
                <p class="text-xs font-bold text-slate-400 uppercase mb-1">Hasil</p>
                <div class="text-3xl font-bold dark:text-white">${Array.isArray(data.result) ? data.result.join(', ') : data.result}</div>
            </div>
            <div>
                <p class="text-xs font-bold text-slate-400 uppercase mb-2">Detail Proses</p>
                <ul class="space-y-2">
                    ${data.steps.map(step => `
                        <li class="flex items-start text-sm text-slate-600 dark:text-slate-400">
                            <svg class="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                            ${step}
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
        el.innerHTML = html;
        container.classList.remove('hidden');
        updateHistory(category, data.formula, data.result);
    };

    // Initial history render
    renderHistory();

    // === API HANDLERS ===
    const callApi = async (url, body) => {
        const r = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        return await r.json();
    };

    // Arithmetic
    const calcArithBtn = document.getElementById('calc-arith');
    if (calcArithBtn) {
        calcArithBtn.addEventListener('click', async () => {
            const a = parseFloat(document.getElementById('a').value) || 0;
            const b = parseFloat(document.getElementById('b').value) || 0;
            const op = document.getElementById('arith-op').value;
            const data = await callApi('/api/arithmetic', { a, b, op });
            if (data.error) alert(data.error);
            else showResult('arith-res', 'arith-res-container', data, 'Aritmatika');
        });
    }

    // Logic
    const calcLogicBtn = document.getElementById('calc-logic');
    if (calcLogicBtn) {
        calcLogicBtn.addEventListener('click', async () => {
            const a = document.getElementById('la').value;
            const b = document.getElementById('lb').value;
            const op = document.getElementById('logic-op').value;
            const data = await callApi('/api/logic', { a, b, op });
            if (data.error) alert(data.error);
            else showResult('logic-res', 'logic-res-container', data, 'Logika');
        });
    }

    // Transform Handlers
    const bindTransform = (btnId, url, bodyFn, category) => {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.addEventListener('click', async () => {
                const data = await callApi(url, bodyFn());
                if (data.error) alert(data.error);
                else {
                    const resEl = document.getElementById(`${btnId}-res-area`);
                    if (resEl) showResult(`${btnId}-res-area`, `${btnId}-res-container`, data, category);
                }
            });
        }
    };

    bindTransform('conv-base', '/api/convert/base', () => ({
        value: document.getElementById('cval').value,
        from: document.getElementById('cfrom').value,
        to: document.getElementById('cto').value
    }), 'Basis');

    bindTransform('conv-temp', '/api/convert/temp', () => ({
        value: parseFloat(document.getElementById('tval').value) || 0,
        from: document.getElementById('tfrom').value,
        to: document.getElementById('tto').value
    }), 'Suhu');

    bindTransform('conv-money', '/api/convert/currency', () => ({
        amount: parseFloat(document.getElementById('mval').value) || 0,
        from: document.getElementById('mfrom').value,
        to: document.getElementById('mto').value
    }), 'Mata Uang');

    bindTransform('calc-fact', '/api/factorial', () => ({
        n: parseInt(document.getElementById('fval').value) || 0
    }), 'Faktorial');

    bindTransform('calc-fib', '/api/fibonacci', () => ({
        n: parseInt(document.getElementById('fn').value) || 0
    }), 'Fibonacci');
});
