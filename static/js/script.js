// static/js/script.js

// Funções de UI
function showLoader(message = "Processando...") {
    document.getElementById('loader-overlay').classList.add('active');
    document.querySelector('.loader-text').textContent = message;
    document.getElementById('loader-progress').style.width = '0%';
    document.getElementById('loader-progress-text').textContent = '0%';
}

function updateLoaderProgress(percent, text = null) {
    document.getElementById('loader-progress').style.width = `${percent}%`;
    document.getElementById('loader-progress-text').textContent = `${percent}%`;
    
    if (text) {
        document.querySelector('.loader-text').textContent = text;
    }
}

function hideLoader() {
    document.getElementById('loader-overlay').classList.remove('active');
}

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });
    document.getElementById(tabName).classList.remove('hidden');
    
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

function showNotification(type, title, message, duration = 5000) {
    const container = document.getElementById('notification-container');
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    let iconClass;
    switch (type) {
        case 'success':
            iconClass = 'fas fa-check-circle';
            break;
        case 'error':
            iconClass = 'fas fa-exclamation-circle';
            break;
        case 'warning':
            iconClass = 'fas fa-exclamation-triangle';
            break;
        case 'info':
            iconClass = 'fas fa-info-circle';
            break;
        default:
            iconClass = 'fas fa-question-circle';
    }
    
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="${iconClass}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    container.appendChild(notification);
    
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'fade-out 0.3s forwards';
        setTimeout(() => {
            container.removeChild(notification);
        }, 300);
    });
    
    if (duration) {
        setTimeout(() => {
            if (notification.parentNode == container) {
                notification.style.animation = 'fade-out 0.3s forwards';
                setTimeout(() => {
                    if (notification.parentNode == container) {
                        container.removeChild(notification);
                    }
                }, 300);
            }
        }, duration);
    }
    
    return notification;
}

function showModal(title, content, confirmCallback, cancelCallback = null) {
    const modal = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const confirmBtn = document.getElementById('modal-confirm');
    const cancelBtn = document.getElementById('modal-cancel');
    const closeBtn = document.querySelector('.modal-close');
    
    modalTitle.textContent = title;
    
    // Limpa o conteúdo anterior
    modalBody.innerHTML = '';
    
    // Se o conteúdo for uma string, insere diretamente
    if (typeof content === 'string') {
        modalBody.innerHTML = content;
    } else {
        // Se for um elemento DOM, anexa ao corpo
        modalBody.appendChild(content);
    }
    
    // Configura os callbacks dos botões
    confirmBtn.onclick = () => {
        if (confirmCallback) confirmCallback();
        hideModal();
    };
    
    cancelBtn.onclick = () => {
        if (cancelCallback) cancelCallback();
        hideModal();
    };
    
    closeBtn.onclick = () => {
        if (cancelCallback) cancelCallback();
        hideModal();
    };
    
    // Mostra o modal
    modal.classList.add('active');
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            if (cancelCallback) cancelCallback();
            hideModal();
        }
    }, { once: true });
}

function hideModal() {
    const modal = document.getElementById('modal-overlay');
    modal.classList.remove('active');
}
function voltarDashboard() {
    window.location.href = '/dashboard';
}

function printPT(ordem) {
    showLoader("Preparando impressão...");
    
    fetch(`/imprimir_pt/${ordem}`, {
        method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
        hideLoader();
        const url = window.URL.createObjectURL(blob);
        window.open(url, '_blank');
    })
    .catch(error => {
        hideLoader();
        console.error('Erro:', error);
        showNotification('error', 'Erro', 'Não foi possível gerar o PDF para impressão.');
    });
}

function retryPT(ordem) {
    showModal(
        'Tentar Novamente',
        `<p>Deseja tentar elaborar novamente a PT para a ordem ${ordem}?</p>`,
        () => {
            showLoader("Reprocessando PT...");
        
            fetch(`/reprocessar_pt/${ordem}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                hideLoader();
                if (data.success) {
                    showNotification('success', 'Sucesso', 'A PT foi reprocessada com sucesso!');
                // Atualiza a página para mostrar o novo status
                    window.location.reload();
                } else {
                    showNotification('error', 'Erro', data.message || 'Erro ao reprocessar a PT.');
                }
            })
            .catch(error => {
                hideLoader();
                console.error('Erro:', error);
                showNotification('error', 'Erro', 'Ocorreu um erro ao tentar reprocessar a PT.');
            });
        }
    );
}

function viewError(ordem) {
    showLoader("Carregando detalhes do erro...");
    
    fetch(`/erro_pt/${ordem}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        
        const errorContent = document.createElement('div');
        errorContent.className = 'error-details';
        
        errorContent.innerHTML = `
            <div class="error-section">
                <h4>Detalhes do Erro</h4>
                <div class="error-message">${data.message}</div>
                <div class="error-timestamp">Ocorrido em: ${data.timestamp}</div>
            </div>
            <div class="error-section">
                <h4>Log Completo</h4>
                <pre class="error-log">${data.log}</pre>
            </div>
            
            <div class="error-section">
                <h4>Sugestões</h4>
                <ul class="error-suggestions">
                ${data.suggestions.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
        showModal(`Erro na PT - ${ordem}`, errorContent);
    })
    .catch(error => {
        hideLoader();
        console.error('Erro:', error);
        showNotification('error', 'Erro', 'Não foi possível carregar os detalhes do erro.');
    });
}

// Funções específicas da aplicação
function filtrarResultados() {
    const statusFilter = document.getElementById('filter-status').value;
    const searchText = document.getElementById('search-order').value.toLowerCase();
    const rows = document.querySelectorAll('#results-table-body tr');
    
    let visibleCount = 0;
    
    rows.forEach(row => {
        const status = row.getAttribute('data-status');
        const ordem = row.cells[0].textContent.toLowerCase();
        const descricao = row.cells[1].textContent.toLowerCase();
        
        const matchesStatus = statusFilter === 'todos' || status === statusFilter;
        const matchesSearch = ordem.includes(searchText) || descricao.includes(searchText);
        
        if (matchesStatus && matchesSearch) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Se não houver resultados, mostrar mensagem
    const tableBody = document.getElementById('results-table-body');
    let noResultsRow = document.getElementById('no-results-row');
    
    if (visibleCount === 0) {
        if (!noResultsRow) {
            noResultsRow = document.createElement('tr');
            noResultsRow.id = 'no-results-row';
            noResultsRow.innerHTML = `
                <td colspan="7" class="no-results">
                    <i class="fas fa-search"></i>
                    <h3>Nenhum resultado encontrado</h3>
                    <p>Tente ajustar os filtros para encontrar o que está procurando.</p>
                </td>
            `;
            tableBody.appendChild(noResultsRow);
        }
    } else if (noResultsRow) {
        noResultsRow.remove();
    }
}

function viewPT(ordem) {
    showLoader("Carregando detalhes da PT...");
    
    fetch(`/detalhes_pt/${ordem}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        
        const detailsContent = document.createElement('div');
        detailsContent.className = 'pt-details';
        
        detailsContent.innerHTML = `
            <div class="details-section">
                <h4>Informações Gerais</h4>
                <div class="details-grid">
                    <div class="detail-item">
                        <div class="detail-label">Ordem</div>
                        <div class="detail-value">${data.ordem}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Número PT</div>
                        <div class="detail-value">${data.numero_pt || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Número AR</div>
                        <div class="detail-value">${data.numero_ar || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Data</div>
                        <div class="detail-value">${data.data}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Status</div>
                        <div class="detail-value">
                            <span class="status-badge status-${data.status.toLowerCase()}">${data.status}</span>
                        </div>
                    </div>
                </div>
            </div>
        
            <div class="details-section">
                <h4>Descrição da Atividade</h4>
                <p>${data.descricao}</p>
            </div>
        
            <div class="details-section">
                <h4>Recomendações</h4>
                <p>${data.recomendacoes || 'Nenhuma recomendação específica.'}</p>
            </div>
        `;
        
        showModal(`Detalhes da PT - ${data.ordem}`, detailsContent);
    })
    .catch(error => {
        hideLoader();
        console.error('Erro:', error);
        showNotification('error', 'Erro', 'Não foi possível carregar os detalhes da PT.');
    });
}

function elaborarPTsComProgresso() {
    const formData = new FormData(document.getElementById('configForm'));
    formData.append('action', 'elaborar_pts');
    
    showLoader("Elaborando PTs...");
    
    fetch('/processar_form', {
        method: 'POST',
        headers: {
            'Accept': 'text/event-stream'
        },
        body: formData
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        function readStream() {
            return reader.read().then(({ value, done }) => {
                if (done) {
                    return;
                }
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\nn');
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.substring(6));
                            
                            if (data.progress !== undefined) {
                                updateLoaderProgress(data.progress, data.message);
                            }
                            
                            if (data.success === true && data.redirect) {
                                hideLoader();
                                window.location.href = data.redirect;
                                return;
                            } else if (data.success === false) {
                                hideLoader();
                                showNotification('error', 'Erro', data.message);
                                return;
                            }
                        } catch (e) {
                            console.error("Erro ao processar resposta:", e);
                        }
                    }
                }
                
                return readStream();
            });
        }
        
        return readStream();
    })
    .catch(error => {
        hideLoader();
        console.error('Erro:', error);
        showNotification('error', 'Erro', 'Ocorreu um erro ao processar a solicitação.');
    });
}


// Função para elaborar PTs
function elaborarPTs() {
    var formData = new FormData(document.getElementById('configForm'));
    formData.append('action', 'elaborar_pts');
    
    showLoader("Elaborando PTs...");
    
    fetch('/processar_form', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let progress = 0;
            
            return new Promise((resolve, reject) => {
                function readChunk() {
                    reader.read().then(({ value, done }) => {
                        if (done) {
                            resolve();
                            return;
                        }
                        
                        const chunk = decoder.decode(value, { stream: true });
                        
                        try {
                            const data = JSON.parse(chunk);
                            if (data.progress) {
                                progress = data.progress;
                                updateLoaderProgress(progress, data.message);
                            }
                        } catch (e) {
                            // Não é JSON ou está incompleto, ignorar
                        }
                        
                        readChunk();
                    }).catch(reject);
                }
                
                readChunk();
            });
        } else {
            throw new Error('Resposta do servidor não ok');
        }
    })
    .then(() => {
        hideLoader();
        // Atualizar a UI com os resultados
        window.location.href = '/resultado';
    })
    .catch(error => {
        console.error('Erro:', error);
        hideLoader();
        alert('Erro ao processar a solicitação. Por favor, tente novamente.');
    });
}
/*function elaborarPTs() {
    const formData = new FormData(document.getElementById('configForm'));
    formData.append('action', 'elaborar_pts');
    
    showLoader("Elaborando PTs...");
    
    fetch('/processar_form', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        
        if (data.success) {
            showNotification('success', 'Sucesso', data.message);
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        } else {
            showNotification('error', 'Erro', data.message);
        }
    })
    .catch(error => {
        hideLoader();
        console.error('Erro:', error);
        showNotification('error', 'Erro', 'Ocorreu um erro ao processar a solicitação.');
    });
}*/


// Outras funções da aplicação
function exportarExcel() {
    showLoader("Exportando dados para Excel...");
    
    fetch('/exportar_excel', {
        method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
        hideLoader();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'resultados_pts.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        
        showNotification('success', 'Excel Exportado', 'Os dados foram exportados com sucesso para Excel.');
    })
    .catch(error => {
        hideLoader();
        console.error('Erro:', error);
        showNotification('error', 'Erro na Exportação', 'Ocorreu um erro ao exportar os dados para Excel.');
    });
}

// Funções específicas de páginas
function confirmarElaborarPT() {
    const form = document.getElementById('configForm');
    const formData = new FormData(form);
    
    // Validação básica do formulário
    const usuario = formData.get('usuario');
    const senha = formData.get('senha');
    const empresa = formData.get('empresa');
    const area = formData.get('area');
    const unidade = formData.get('unidade');
    const arquivo = document.getElementById('arquivo').files[0];
    
    if (!usuario || !senha || !empresa || !area || !unidade) {
        showNotification('warning', 'Campos Incompletos', 'Por favor, preencha todos os campos obrigatórios.');
        return;
    }
    
    if (!arquivo) {
        showNotification('warning', 'Arquivo Não Selecionado', 'Por favor, selecione um arquivo Excel com as ordens de trabalho.');
        return;
    }
    
    // Exibe modal de confirmação
    showModal(
        'Confirmar Elaboração de PT',
        `<p>Você está prestes a elaborar Permissões de Trabalho com os seguintes parâmetros:</p>
        <ul>
            <li><strong>Empresa:</strong> ${empresa}</li>
            <li><strong>Área:</strong> ${area}</li>
            <li><strong>Unidade:</strong> ${unidade}</li>
            <li><strong>Arquivo:</strong> ${arquivo.name}</li>
        </ul>
        <p>Este processo pode levar alguns minutos, dependendo da quantidade de PTs a serem elaboradas.</p>
        <p>Deseja continuar?</p>`,
        () => {
            // Callback de confirmação - inicia a elaboração
            elaborarPTs();
        }
    );
}

// Função para lidar com mudanças na seleção de arquivos
function handleFileSelect(event) {
    const fileInput = event.target;
    const fileLabel = document.getElementById('file-label');
    const fileIcon = document.getElementById('file-icon');
    
    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        fileLabel.textContent = fileName;
        fileLabel.title = fileName;
        fileIcon.className = 'fas fa-file-excel'; // Altera o ícone para Excel
        
        // Exibe informações do arquivo
        document.getElementById('file-info').classList.remove('hidden');
        document.getElementById('file-name').textContent = fileName;
        document.getElementById('file-size').textContent = formatFileSize(fileInput.files[0].size);
    } else {
        fileLabel.textContent = 'Selecionar arquivo';
        fileLabel.title = '';
        fileIcon.className = 'fas fa-upload';
        
        // Esconde informações do arquivo
        document.getElementById('file-info').classList.add('hidden');
    }
}

// Função para formatar o tamanho do arquivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Configurar ouvintes de eventos para filtros
    const filterStatus = document.getElementById('filter-status');
    const searchOrder = document.getElementById('search-order');
    
    if (filterStatus) {
        filterStatus.addEventListener('change', filtrarResultados);
    }
    
    if (searchOrder) {
        searchOrder.addEventListener('input', filtrarResultados);
    }
    
    // Configurar ouvintes de eventos para arquivos
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', handleFileSelect);
    });
    
    // Inicializar tabs se existirem
    const tabs = document.querySelectorAll('.tab');
    if (tabs.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function(event) {
                const tabName = this.getAttribute('data-tab');
                showTab(tabName);
            });
        });
        
        // Ativar a primeira tab por padrão
        tabs[0].click();
    }
    
    // Inicializar selects customizados
    const customSelects = document.querySelectorAll('.custom-select');
    customSelects.forEach(select => {
        const selectElement = select.querySelector('select');
        const customSelected = select.querySelector('.select-selected');
        const customOptions = select.querySelector('.select-items');
        
        if (selectElement && customSelected && customOptions) {
            // Atualiza o texto do elemento selecionado
            customSelected.textContent = selectElement.options[selectElement.selectedIndex].text;
            
            // Cria os elementos de opção personalizados
            Array.from(selectElement.options).forEach((option, index) => {
                const optionDiv = document.createElement('div');
                optionDiv.textContent = option.text;
                optionDiv.setAttribute('data-value', option.value);
                
                if (index === selectElement.selectedIndex) {
                    optionDiv.className = 'same-as-selected';
                }
                
                optionDiv.addEventListener('click', function() {
                    selectElement.value = this.getAttribute('data-value');
                    customSelected.textContent = this.textContent;
                    
                    // Atualiza a classe do item selecionado
                    const selectedItem = customOptions.querySelector('.same-as-selected');
                    if (selectedItem) {
                        selectedItem.classList.remove('same-as-selected');
                    }
                    this.classList.add('same-as-selected');
                    
                    // Dispara o evento change no select original
                    const event = new Event('change', { bubbles: true });
                    selectElement.dispatchEvent(event);
                    
                    // Fecha o dropdown
                    customOptions.classList.remove('select-show');
                });
                
                customOptions.appendChild(optionDiv);
            });
            
            // Evento para abrir/fechar o dropdown
            customSelected.addEventListener('click', function(e) {
                e.stopPropagation();
                customOptions.classList.toggle('select-show');
                this.classList.toggle('select-arrow-active');
            });
            
            // Fecha o dropdown quando clicar fora dele
            document.addEventListener('click', function() {
                customOptions.classList.remove('select-show');
                customSelected.classList.remove('select-arrow-active');
            });
        }
    });
});