<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Response, make_response
import time
import json
import datetime
import os
from werkzeug.utils import secure_filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import numpy as np
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import filedialog, messagebox
import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
import webbrowser
import json

# Importações do módulo elaborador (assumindo que o módulo existe)
from elaborador import (
    elaborar_pts,
    consultar_ar,
    elaborar_ar,
)

# Variáveis globais
usuario = ""
senha = ""
data = ""
caminho_arquivo = ""
df = None  # DataFrame global
especialidades = []  # Lista global para armazenar as especialidades únicas

# Criar aplicação Flask
app = Flask(__name__)
app.secret_key = 'J0@0P@uloFla'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.static_folder = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Garante que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configurar pasta de templates
app.template_folder = 'templates'

# Configurar pasta de arquivos estáticos
app.static_folder = 'static'

# Criar pasta de templates se não existir
if not os.path.exists('templates'):
    os.makedirs('templates')

# Criar pasta de arquivos estáticos se não existir
if not os.path.exists('static'):
    os.makedirs('static')

# Criar arquivo CSS básico
css_content = """
:root {
  --petrobras-green: #009846;
  --petrobras-green-dark: #006633;
  --petrobras-yellow: #FCCE03;
  --petrobras-blue: #0064AF;
  --petrobras-gray: #58595B;
  --petrobras-light-gray: #F2F2F2;
}
body {
  font-family: 'Open Sans', Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: var(--petrobras-light-gray);
  color: #333;
}
.container {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
}
.sidebar {
    flex: 1;
    min-width: 300px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 20px;
}
.content {
    flex: 3;
    display: flex;
    flex-direction: column;
    min-width: 600px;
}
/* Responsividade */
@media (max-width: 992px) {
  .container {
    flex-direction: column;
  }
  
  .sidebar, .content {
    min-width: 100%;
  }
}
.tabs {
    display: flex;
    margin-bottom: 10px;
}
.tab {
    padding: 10px 20px;
    background-color: #ddd;
    border: none;
    cursor: pointer;
    margin-right: 5px;
    border-radius: 5px 5px 0 0;
}
.tab.active {
    background-color: #fff;
}
.tab-content {
    display: flex;
    flex: 1;
}
.gallery {
    flex: 1;
    background-color: #e0e0e0;
    padding: 10px;
    border-radius: 5px;
    margin-right: 10px;
    overflow-y: auto;
    max-height: 600px;
}
.result {
    flex: 2;
    background-color: #d0d0d0;
    padding: 10px;
    border-radius: 5px;
    overflow-y: auto;
    max-height: 600px;
}
.button {
    background-color: var(--petrobras-green);
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}
.button:hover {
  background-color: var(--petrobras-green-dark);
}
.button-blue {
    background-color: var(--petrobras-blue);
}
.button-orange {
    background-color: var(--petrobras-yellow);
    color: #333;
}
.header {
    background-color: var(--petrobras-green);
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header img {
    height: 90px;
}
.text-button {
    background: none;
    border: none;
    color: #2196F3;
    padding: 5px;
    text-align: left;
    text-decoration: underline;
    display: block;
    font-size: 16px;
    margin: 2px 0;
    cursor: pointer;
}
input[type=text], input[type=password], input[type=date], select {
  width: 100%;
  padding: 12px;
  margin: 8px 0 16px;
  display: block;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 16px;
  transition: border-color 0.3s;
}
input[type=text]:focus, input[type=password]:focus, input[type=date]:focus, select:focus {
  border-color: var(--petrobras-green);
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 152, 70, 0.2);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
  color: var(--petrobras-gray);
}

.form-control {
  position: relative;
}

.form-control .icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--petrobras-gray);
}

.file-input-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  margin: 15px 0;
}

.file-input-wrapper input[type=file] {
  position: absolute;
  font-size: 100px;
  opacity: 0;
  right: 0;
  top: 0;
  cursor: pointer;
}

.file-input-button {
  display: inline-block;
  background-color: var(--petrobras-blue);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.file-name {
  margin-left: 10px;
  font-style: italic;
}
/* Adicione ao style.css */
.tabs {
  display: flex;
  background-color: white;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  margin-bottom: 0;
  box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
}

.tab {
  padding: 15px 25px;
  background-color: white;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: var(--petrobras-gray);
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
}

.tab.active {
  color: var(--petrobras-green);
  border-bottom: 3px solid var(--petrobras-green);
}

.tab:hover:not(.active) {
  background-color: #f9f9f9;
  color: #333;
}

.tab-content {
  background-color: white;
  border-radius: 0 0 8px 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  flex: 1;
  gap: 20px;
}
/* Adicione ao style.css */
.gallery, .result {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  overflow-y: auto;
  max-height: 600px;
}

.gallery {
  flex: 1;
  border-left: 4px solid var(--petrobras-blue);
}

.result {
  flex: 2;
  border-left: 4px solid var(--petrobras-green);
}

.text-button {
  background: none;
  border: none;
  color: var(--petrobras-blue);
  padding: 8px 12px;
  text-align: left;
  display: block;
  font-size: 15px;
  margin: 2px 0;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
  width: 100%;
}

.text-button:hover {
  background-color: rgba(0, 100, 175, 0.1);
}

.data-card {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
  border-left: 4px solid var(--petrobras-green);
}

.data-card h3 {
  margin-top: 0;
  color: var(--petrobras-gray);
  font-size: 18px;
}

.data-card p {
  margin: 8px 0;
  font-size: 14px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.status-emitida {
  background-color: var(--petrobras-green);
  color: white;
}

.status-elaborar {
  background-color: var(--petrobras-yellow);
  color: #333;
}

.status-erro {
  background-color: #e74c3c;
  color: white;
}

/* Tabela de resultados */
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
}

.data-table th {
  background-color: var(--petrobras-light-gray);
  color: var(--petrobras-gray);
  font-weight: 600;
  text-align: left;
  padding: 12px 15px;
}

.data-table td {
  border-bottom: 1px solid #eee;
  padding: 10px 15px;
}

.data-table tr:hover {
  background-color: rgba(0, 152, 70, 0.05);
}

.data-table .actions {
  display: flex;
  gap: 8px;
}

.data-table .action-button {
  background: none;
  border: none;
  color: var(--petrobras-blue);
  cursor: pointer;
  font-size: 16px;
}

.data-table .action-button:hover {
  color: var(--petrobras-green);
}

.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-actions {
  display: flex;
  gap: 10px;
}

.dashboard-stats {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 200px;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 28px;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--petrobras-green);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--petrobras-gray);
  font-size: 14px;
}

.dashboard-content {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.recent-activities, .upcoming-tasks {
  flex: 1;
  min-width: 300px;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.activity-list {
  margin-top: 15px;
}

.activity-item {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.activity-icon {
  width: 40px;
  height: 40px;
  background-color: var(--petrobras-light-gray);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 18px;
}

.activity-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.activity-desc {
  font-size: 14px;
  color: var(--petrobras-gray);
}

.activity-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.loader-overlay.active {
  opacity: 1;
  visibility: visible;
}

.loader-container {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  max-width: 80%;
  width: 400px;
}

.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid var(--petrobras-green);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loader-text {
  font-size: 18px;
  margin-bottom: 15px;
  color: var(--petrobras-gray);
}

.loader-progress-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--petrobras-green);
  margin-bottom: 10px;
}

.loader-progress-bar {
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  overflow: hidden;
}

.loader-progress-fill {
  height: 100%;
  background-color: var(--petrobras-green);
  width: 0%;
  transition: width 0.3s ease-in-out;
}
/* Adicione ao style.css */
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 300px;
  z-index: 1000;
}

.notification {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16);
  animation: slide-in 0.3s ease-out forwards;
  position: relative;
  display: flex;
  align-items: flex-start;
}

.notification-success {
  background-color: #d4edda;
  border-left: 4px solid var(--petrobras-green);
  color: #155724;
}

.notification-error {
  background-color: #f8d7da;
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.notification-warning {
  background-color: #fff3cd;
  border-left: 4px solid var(--petrobras-yellow);
  color: #856404;
}

.notification-info {
  background-color: #d1ecf1;
  border-left: 4px solid var(--petrobras-blue);
  color: #0c5460;
}

.notification-icon {
  margin-right: 10px;
  font-size: 20px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.notification-message {
  font-size: 14px;
}

.notification-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 18px;
  opacity: 0.5;
  padding: 0;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fade-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}
/* Adicione ao style.css */
.results-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-actions {
  display: flex;
  gap: 10px;
}

.results-summary {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.summary-card {
  flex: 1;
  min-width: 200px;
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
}

.summary-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
}

.summary-icon.success {
  background-color: rgba(0, 152, 70, 0.1);
  color: var(--petrobras-green);
}

.summary-icon.warning {
  background-color: rgba(252, 206, 3, 0.1);
  color: #856404;
}

.summary-icon.error {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.summary-icon.info {
  background-color: rgba(0, 100, 175, 0.1);
  color: var(--petrobras-blue);
}

.summary-content {
  flex: 1;
}

.summary-title {
  font-size: 14px;
  color: var(--petrobras-gray);
  margin-bottom: 5px;
}

.summary-number {
  font-size: 24px;
  font-weight: 700;
}

.results-filter {
  display: flex;
  gap: 20px;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  font-weight: 600;
  color: var(--petrobras-gray);
  white-space: nowrap;
}

.filter-group select, .filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.results-table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.results-table {
  margin: 0;
}

.results-table td {
  vertical-align: middle;
}

.no-results {
  padding: 40px;
  text-align: center;
  color: var(--petrobras-gray);
}

.no-results i {
  font-size: 48px;
  margin-bottom: 15px;
  color: #ddd;
}

.no-results h3 {
  margin-bottom: 10px;
}

.no-results p {
  max-width: 400px;
  margin: 0 auto;
}
/* Estilos para os detalhes da PT e erros */
.pt-details, .error-details {
  width: 100%;
}

.details-section, .error-section {
  margin-bottom: 20px;
}

.details-section h4, .error-section h4 {
  color: var(--petrobras-green);
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
  margin-top: 0;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 12px;
  color: var(--petrobras-gray);
  margin-bottom: 5px;
}

.detail-value {
  font-weight: 600;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 10px;
  font-weight: 600;
}

.error-timestamp {
  font-size: 12px;
  color: var(--petrobras-gray);
  text-align: right;
}

.error-log {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  max-height: 200px;
  overflow-y: auto;
  font-size: 12px;
}

.error-suggestions li {
  margin-bottom: 8px;
}
/* Adicione ao style.css */
.main-container {
  display: flex;
  min-height: calc(100vh - 70px);
}

.sidebar {
  width: 250px;
  background-color: white;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.nav-menu {
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: var(--petrobras-gray);
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: rgba(0, 152, 70, 0.05);
  color: var(--petrobras-green);
}

.nav-item.active {
  background-color: rgba(0, 152, 70, 0.1);
  color: var(--petrobras-green);
  border-left-color: var(--petrobras-green);
  font-weight: 600;
}

.nav-item i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.sidebar-info {
  margin-top: auto;
  padding: 20px;
  border-top: 1px solid #eee;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: var(--petrobras-gray);
  font-size: 14px;
}

.info-item i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: var(--petrobras-light-gray);
  overflow-x: hidden;
}

.breadcrumb {
  background-color: white;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  font-size: 14px;
}

.breadcrumb a {
  color: var(--petrobras-blue);
  text-decoration: none;
}

.breadcrumb-separator {
  margin: 0 10px;
  color: #ccc;
}

.breadcrumb-current {
  color: var(--petrobras-gray);
  font-weight: 600;
}

.content {
  flex: 1;
}

.footer {
  margin-top: 30px;
  padding: 15px 0;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  color: var(--petrobras-gray);
  font-size: 14px;
}

.logout-btn {
  margin-left: 15px;
  color: #dc3545;
  text-decoration: none;
  font-size: 14px;
}

.logout-btn:hover {
  text-decoration: underline;
}

/* Responsividade */
@media (max-width: 992px) {
  .main-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .nav-menu {
    display: flex;
    overflow-x: auto;
    padding: 10px;
  }
  
  .nav-item {
    padding: 10px 15px;
    border-left: none;
    border-bottom: 3px solid transparent;
    white-space: nowrap;
  }
  
  .nav-item.active {
    border-left-color: transparent;
    border-bottom-color: var(--petrobras-green);
  }
  
  .sidebar-info {
    display: none;
  }
  
  .header {
    flex-direction: column;
    text-align: center;
    padding: 10px;
  }
  
  .header-title h1 {
    font-size: 18px;
    margin: 10px 0;
  }
  
  .user-info {
    margin-top: 10px;
  }
}
/* Adicione ao style.css */
.login-page {
  background-color: var(--petrobras-light-gray);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 1000px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-header {
  background-color: var(--petrobras-green);
  color: white;
  padding: 20px;
  text-align: center;
}

.login-logo {
  height: 60px;
  margin-bottom: 15px;
}

.login-header h1 {
  font-size: 24px;
  margin: 0;
  font-weight: 600;
}

.login-form-container {
  display: flex;
}

.login-form-wrapper {
  flex: 1;
  padding: 30px;
  border-right: 1px solid #eee;
}

.login-form-wrapper h2 {
  color: var(--petrobras-green);
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 22px;
}

.login-info {
  flex: 1;
  padding: 30px;
  background-color: #f9f9f9;
}

.info-box {
  margin-bottom: 30px;
}

.info-box h3 {
  color: var(--petrobras-blue);
  font-size: 18px;
  margin-top: 0;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.info-box h3 i {
  margin-right: 10px;
}

.info-box p {
  color: var(--petrobras-gray);
  margin-bottom: 10px;
  line-height: 1.5;
}

.info-box ul {
  padding-left: 20px;
  color: var(--petrobras-gray);
}

.info-box li {
  margin-bottom: 8px;
}

.info-box li i {
  margin-right: 10px;
  color: var(--petrobras-blue);
}

.login-footer {
  background-color: #f2f2f2;
  padding: 15px;
  text-align: center;
  border-top: 1px solid #eee;
  color: var(--petrobras-gray);
  font-size: 14px;
}

.login-footer p {
  margin: 5px 0;
}

.login-error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.login-error i {
  margin-right: 10px;
  font-size: 18px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.remember-me {
  display: flex;
  align-items: center;
}

.remember-me input {
  margin-right: 8px;
}

.forgot-password {
  color: var(--petrobras-blue);
  text-decoration: none;
  font-size: 14px;
}

.forgot-password:hover {
  text-decoration: underline;
}

.button-full {
  width: 100%;
}

/* Responsividade */
@media (max-width: 768px) {
  .login-form-container {
    flex-direction: column;
  }
  
  .login-form-wrapper {
    border-right: none;
    border-bottom: 1px solid #eee;
  }
}
/* Adicione ao style.css */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: var(--petrobras-green);
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--petrobras-gray);
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.button-outline {
  background-color: transparent;
  border: 1px solid var(--petrobras-green);
  color: var(--petrobras-green);
}

.button-outline:hover {
  background-color: rgba(0, 152, 70, 0.1);
}
/* Adicione ao style.css */
.page-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.page-header h2 {
  color: var(--petrobras-green);
  margin: 0;
}

.form-container {
  margin-bottom: 30px;
}

.config-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 20px;
  border: 1px solid #eee;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: var(--petrobras-gray);
  font-size: 18px;
}

.form-row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 10px;
}

.button-small {
  padding: 5px 10px;
  font-size: 14px;
}

.file-preview {
  margin-top: 15px;
  background-color: white;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 15px;
}

.file-preview h4 {
  margin-top: 0;
  color: var(--petrobras-gray);
  font-size: 16px;
  margin-bottom: 10px;
}

.preview-info {
  margin-bottom: 15px;
}

.preview-info p {
  margin: 5px 0;
}

.preview-actions {
  text-align: right;
}

.resultado-container {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
  border: 1px solid #eee;
}


.hidden {
    display: none;
}
"""

# Criar arquivo CSS
with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# Criar arquivo HTML básico
html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acompanhamento de PTs</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="header">
        <div class="logo">
            <img src="{{ url_for('static', filename='logo-petrobras.png') }}" alt="Petrobras">
        </div>
        <div class="header-title">
            <h1>Sistema de Gestão de Permissões de Trabalho</h1>
        </div>
        <div class="user-info">
            <span id="username">Usuário: </span>
        </div>
    </div>

    <div class="container">
        <div class="sidebar">
            <h2>Informações</h2>
            <form id="configForm" method="post" enctype="multipart/form-data" action="{{ url_for('processar_form') }}">
                <label for="usuario">Usuário:</label>
                <input type="text" id="usuario" name="usuario" required>
                
                <label for="senha">Senha:</label>
                <input type="password" id="senha" name="senha" required>
                
                <label for="empresa">Empresa:</label>
                <select id="empresa" name="empresa">
                    <option value="PETROBRAS">PETROBRAS</option>
                </select>
                
                <label for="area">Área ou Gerência:</label>
                <select id="area" name="area" onchange="atualizarUnidade()">
                    <option value="GAS NATURAL&ENERGIA">GAS NATURAL&ENERGIA</option>
                    <option value="REFINO">REFINO</option>
                </select>
                
                <div id="unidadeGasNatural">
                    <label for="unidadeGas">Unidade:</label>
                    <select id="unidadeGas" name="unidadeGas">
                        <option value="UTE-BF">UTE-BF</option>
                        <option value="UTE-CAN">UTE-CAN</option>
                        <option value="UTE-CBT">UTE-CBT</option>
                        <option value="UTE-IBT">UTE-IBT</option>
                        <option value="UTE-JF">UTE-JF</option>
                        <option value="UTE-NPI">UTE-NPI</option>
                        <option value="UTE-SRP">UTE-SRP</option>
                        <option value="UTE-TBA-TCA">UTE-TBA-TCA</option>
                        <option value="UTE-TCE">UTE-TCE</option>
                        <option value="UTE-TLG">UTE-TLG</option>
                        <option value="UTE-TMA">UTE-TMA</option>
                        <option value="UTE-TRI">UTE-TRI</option>
                        <option value="UTE-VLA">UTE-VLA</option>
                        <option value="UTGC e UTGSUL">UTGC e UTGSUL</option>
                        <option value="UTGCA">UTGCA</option>
                        <option value="UTGCAB">UTGCAB</option>
                        <option value="UTGITB">UTGITB</option>
                    </select>
                </div>
                
                <div id="unidadeRefino" class="hidden">
                    <label for="unidadeRef">Unidade:</label>
                    <select id="unidadeRef" name="unidadeRef">
                        <option value="FAFEN-BA">FAFEN-BA</option>
                        <option value="FAFEN-SE">FAFEN-SE</option>
                        <option value="LUBNOR">LUBNOR</option>
                        <option value="PROTEGE+">PROTEGE+</option>
                        <option value="RECAP">RECAP</option>
                        <option value="REDUC">REDUC</option>
                        <option value="REFAP">REFAP</option>
                        <option value="REGAP">REGAP</option>
                        <option value="REMAN">REMAN</option>
                        <option value="REPAR">REPAR</option>
                        <option value="REPLAN">REPLAN</option>
                        <option value="REVAP">REVAP</option>
                        <option value="RLAM">RLAM</option>
                        <option value="RNEST">RNEST</option>
                        <option value="RPBC">RPBC</option>
                        <option value="SIX">SIX</option>
                    </select>
                </div>
                
                <label for="data">Data para emissão:</label>
                <input type="date" id="data" name="data">
                
                <input type="file" id="planilha" name="planilha" accept=".xlsx,.xls">
                
                <div id="status"></div>
                
                <div>
                    <button type="button" class="button" onclick="elaborarPTs()">Elaborar PTs</button>
                    <button type="button" class="button button-blue" onclick="consultarAR()">Consultar AR</button>
                    <button type="button" class="button button-orange" onclick="elaborarAR()">Elaborar AR</button>
                </div>
                
                <div id="resultado"></div>
            </form>
        </div>
        
        <div class="content">
            <div class="tabs">
                <button class="tab active" onclick="showTab('acompanhamento')">Acompanhamento da Programação</button>
                <button class="tab" onclick="showTab('elaboracao')">Elaboração de AR</button>
            </div>
            
            <div id="acompanhamento" class="tab-content">
                <div class="gallery" id="galeria">
                    <!-- Especialidades serão carregadas aqui -->
                </div>
                <div class="result" id="resultado-acompanhamento">
                    <!-- Resultados serão exibidos aqui -->
                </div>
            </div>
            
            <div id="elaboracao" class="tab-content hidden">
                <div class="gallery" id="galeria-elaboracao">
                    <!-- Especialidades serão carregadas aqui para elaboração -->
                </div>
                <div class="result" id="resultado-elaboracao">
                    <!-- Resultados de elaboração serão exibidos aqui -->
                </div>
            </div>
        </div>
    </div>
    <div id="loader-overlay" class="loader-overlay">
        <div class="loader-container">
            <div class="loader"></div>
            <div class="loader-text">Processando...</div>
            <div id="loader-progress-text" class="loader-progress-text">0%</div>
            <div class="loader-progress-bar">
            <div id="loader-progress" class="loader-progress-fill"></div>
            </div>
        </div>
    </div>
    <div id="notification-container" class="notification-container"></div>
    <div id="modal-overlay" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 id="modal-title">Título do Modal</h3>
                <button class="modal-close">&times;</button>
            </div>
            <div class="modal-body" id="modal-body">
                Conteúdo do modal
            </div>
            <div class="modal-footer">
                <button class="button button-outline" id="modal-cancel">Cancelar</button>
                <button class="button" id="modal-confirm">Confirmar</button>
            </div>
        </div>
    </div>
    
    <script>
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
        function voltarDashboard() {
            window.location.href = '/dashboard';
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
                    iconClass = 'ℹ️';
                    break;
                default:
                    iconClass = '?';
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
        function atualizarUnidade() {
            var area = document.getElementById('area').value;
            if (area === 'GAS NATURAL&ENERGIA') {
                document.getElementById('unidadeGasNatural').classList.remove('hidden');
                document.getElementById('unidadeRefino').classList.add('hidden');
            } else {
                document.getElementById('unidadeGasNatural').classList.add('hidden');
                document.getElementById('unidadeRefino').classList.remove('hidden');
            }
        }
        
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

        
        function consultarAR() {
            var formData = new FormData(document.getElementById('configForm'));
            formData.append('action', 'consultar_ar');
            
            fetch('/processar_form', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('resultado').innerText = data.message;
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('resultado').innerText = 'Erro ao processar a solicitação.';
            });
        }
        
        function elaborarAR() {
            var formData = new FormData(document.getElementById('configForm'));
            formData.append('action', 'elaborar_ar');
            
            fetch('/processar_form', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('resultado').innerText = data.message;
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('resultado').innerText = 'Erro ao processar a solicitação.';
            });
        }
        
        function carregarEspecialidades() {
            fetch('/especialidades')
            .then(response => response.json())
            .then(data => {
                const galeriaDiv = document.getElementById('galeria');
                const galeriaElaboracaoDiv = document.getElementById('galeria-elaboracao');
                
                galeriaDiv.innerHTML = '';
                galeriaElaboracaoDiv.innerHTML = '';
                
                data.especialidades.forEach(esp => {
                    // Para aba de acompanhamento
                    const btn = document.createElement('button');
                    btn.className = 'text-button';
                    btn.innerText = esp;
                    btn.onclick = function() { exibirOpcoesOrdem(esp); };
                    galeriaDiv.appendChild(btn);
                    
                    // Para aba de elaboração
                    const btnElab = document.createElement('button');
                    btnElab.className = 'text-button';
                    btnElab.innerText = esp;
                    btnElab.onclick = function() { exibirAnalisesPendentes(esp); };
                    galeriaElaboracaoDiv.appendChild(btnElab);
                });
            })
            .catch(error => {
                console.error('Erro ao carregar especialidades:', error);
            });
        }
        
        function exibirOpcoesOrdem(especialidade) {
            fetch(`/ordens/${especialidade}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-acompanhamento');
                resultadoDiv.innerHTML = '';
                
                data.ordens.forEach(ordem => {
                    const btn = document.createElement('button');
                    btn.className = 'text-button';
                    btn.innerText = `Ordem: ${ordem}`;
                    btn.onclick = function() { mostrarDetalhes(especialidade, ordem); };
                    resultadoDiv.appendChild(btn);
                                });
            })
            .catch(error => {
                console.error('Erro ao carregar ordens:', error);
            });
        }
        
        function mostrarDetalhes(especialidade, ordem) {
            fetch(`/detalhes/${especialidade}/${ordem}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-acompanhamento');
                resultadoDiv.innerHTML = '';
                
                if (data.detalhes.length > 0) {
                    data.detalhes.forEach(detalhe => {
                        // Adiciona a Ordem
                        const ordemText = document.createElement('h3');
                        ordemText.innerText = `Ordem: ${detalhe.ordem}`;
                        resultadoDiv.appendChild(ordemText);
                        
                        // Adiciona a Descrição
                        const descText = document.createElement('p');
                        descText.innerText = `Descrição da PT: ${detalhe.descricao}`;
                        resultadoDiv.appendChild(descText);
                        
                        // Adiciona LIBRA, ARO e AR
                        const infoText = document.createElement('p');
                        infoText.innerText = `LIBRA: ${detalhe.libra}, ARO: ${detalhe.aro}, Análise de Risco: ${detalhe.ar}`;
                        resultadoDiv.appendChild(infoText);
                        
                        // Separador
                        const divider = document.createElement('hr');
                        resultadoDiv.appendChild(divider);
                    });
                } else {
                    const noDataText = document.createElement('p');
                    noDataText.innerText = `Nenhum detalhe encontrado para a Especialidade ${especialidade} e Ordem ${ordem}.`;
                    resultadoDiv.appendChild(noDataText);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar detalhes:', error);
            });
        }
        
        function exibirAnalisesPendentes(especialidade) {
            fetch(`/analises_pendentes/${especialidade}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-elaboracao');
                resultadoDiv.innerHTML = '';
                
                data.numeros_ar.forEach(numero_ar => {
                    const btn = document.createElement('button');
                    btn.className = 'text-button';
                    btn.innerText = `Número A.R.: ${numero_ar}`;
                    btn.onclick = function() { mostrarDetalhesElaboracao(especialidade, numero_ar); };
                    resultadoDiv.appendChild(btn);
                });
            })
            .catch(error => {
                console.error('Erro ao carregar análises pendentes:', error);
            });
        }
        
        function mostrarDetalhesElaboracao(especialidade, numero_ar) {
            fetch(`/detalhes_elaboracao/${especialidade}/${numero_ar}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-elaboracao');
                resultadoDiv.innerHTML = '';
                
                if (data.detalhes.length > 0) {
                    data.detalhes.forEach(detalhe => {
                        // Container principal para todos os componentes
                        const containerPrincipal = document.createElement('div');
                        
                        // Adiciona o Número A.R.
                        const numeroARText = document.createElement('h3');
                        numeroARText.innerText = `Número A.R.: ${detalhe.numero_ar}`;
                        containerPrincipal.appendChild(numeroARText);
                        
                        // Adiciona a Ordem
                        const ordemText = document.createElement('h4');
                        ordemText.innerText = `Ordem: ${detalhe.ordem}`;
                        containerPrincipal.appendChild(ordemText);
                        
                        // Campo para Serviço
                        const servicoLabel = document.createElement('label');
                        servicoLabel.innerText = 'Serviço:';
                        containerPrincipal.appendChild(servicoLabel);
                        
                        const servicoInput = document.createElement('input');
                        servicoInput.type = 'text';
                        servicoInput.value = detalhe.servico || '';
                        servicoInput.id = `servico-${detalhe.id}`;
                        containerPrincipal.appendChild(servicoInput);
                        
                        // Campo para Equipamento
                        const equipamentoLabel = document.createElement('label');
                        equipamentoLabel.innerText = 'Equipamento:';
                        containerPrincipal.appendChild(equipamentoLabel);
                        
                        const equipamentoInput = document.createElement('input');
                        equipamentoInput.type = 'text';
                        equipamentoInput.value = detalhe.equipamento || '';
                        equipamentoInput.id = `equipamento-${detalhe.id}`;
                        containerPrincipal.appendChild(equipamentoInput);
                        
                        // Dropdown para Executante
                        const executanteLabel = document.createElement('label');
                        executanteLabel.innerText = 'Executante:';
                        containerPrincipal.appendChild(executanteLabel);
                        
                        const executanteSelect = document.createElement('select');
                        executanteSelect.id = `executante-${detalhe.id}`;
                        ['Executante 1', 'Executante 2'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.executante === opt) {
                                option.selected = true;
                            }
                            executanteSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(executanteSelect);
                        
                        // Dropdown para Operador
                        const operadorLabel = document.createElement('label');
                        operadorLabel.innerText = 'Operador:';
                        containerPrincipal.appendChild(operadorLabel);
                        
                        const operadorSelect = document.createElement('select');
                        operadorSelect.id = `operador-${detalhe.id}`;
                        ['Operador 1', 'Operador 2'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.operador === opt) {
                                option.selected = true;
                            }
                            operadorSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(operadorSelect);
                        
                        // Dropdown para SMS
                        const smsLabel = document.createElement('label');
                        smsLabel.innerText = 'SMS:';
                        containerPrincipal.appendChild(smsLabel);
                        
                        const smsSelect = document.createElement('select');
                        smsSelect.id = `sms-${detalhe.id}`;
                        ['SMS 1', 'SMS 2'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.sms === opt) {
                                option.selected = true;
                            }
                            smsSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(smsSelect);
                        
                        // Dropdown para Perigos
                        const perigoLabel = document.createElement('label');
                        perigoLabel.innerText = 'Perigos:';
                        containerPrincipal.appendChild(perigoLabel);
                        
                        const perigoSelect = document.createElement('select');
                        perigoSelect.id = `perigo-${detalhe.id}`;
                        ['Queda', 'Choque Elétrico', 'Incêndio'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.perigo === opt) {
                                option.selected = true;
                            }
                            perigoSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(perigoSelect);
                        
                        // Botão para mostrar/ocultar as opções
                        const btnToggleOpcoes = document.createElement('button');
                        btnToggleOpcoes.className = 'button';
                        btnToggleOpcoes.innerText = 'Mostrar Opções';
                        btnToggleOpcoes.onclick = function() {
                            const containerOpcoes = document.getElementById(`opcoes-${detalhe.id}`);
                            containerOpcoes.classList.toggle('hidden');
                            btnToggleOpcoes.innerText = containerOpcoes.classList.contains('hidden') ? 'Mostrar Opções' : 'Ocultar Opções';
                        };
                        containerPrincipal.appendChild(btnToggleOpcoes);
                        
                        // Container para as opções (checkboxes)
                        const containerOpcoes = document.createElement('div');
                        containerOpcoes.id = `opcoes-${detalhe.id}`;
                        containerOpcoes.className = 'hidden';
                        
                        // Lista de perguntas
                        const perguntas = [
                            "Falta procedimento específico ou padrão básico de segurança para execução da intervenção ou é necessário alterar o padrão de execução existente?",
                            "A intervenção é realizada em local não projetado para ocupação humana contínua ou possua meios limitados de entrada e saída ou a ventilação existente é insuficiente para remover contaminantes ou possa existir a deficiência ou enriquecimento de oxigênio?",
                            "Na intervenção pode haver contato direto com produtos inflamáveis ou tóxicos?",
                            "A intervenção será realizada em instalação elétrica energizada com tensão igual ou superior a 50Vca ou 120 Vcc de forma não prevista em padrão de execução específico?",
                            "Na intervenção pode haver contato com partes desprotegidas de equipamento ou com alta temperatura ou pressurizado?",
                            "No local da intervenção existe mais de uma disciplina de manutenção ou engenharia atuando simultaneamente que acarretem riscos às equipes ou a equipamentos/sistemas vizinhos?",
                            "A elevação de carga é considerada movimentação crítica conforme padrão PE-1PBR-1428?",
                            "A intervenção envolve escavações, perfurações, fundações, de forma não prevista no padrão PE-1PBR-01426 - Segurança em Serviços de Escavação e Intervenção no Solo?",
                            "A intervenção é realizada em local acima de 2m do piso de referência (nível, superfície ou plataforma considerada como nível zero para caracterização do trabalho em altura) de forma não prevista em padrão de execução específico e na NR-35 e expõe o trabalhador a risco de queda?"
                        ];
                        
                        // Adiciona as opções ao container de opções
                        perguntas.forEach((pergunta, idx) => {
                            const checkboxRow = document.createElement('div');
                            
                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.id = `opcao-${detalhe.id}-${idx + 1}`;
                            checkbox.checked = detalhe[`opcao_${idx + 1}`] || false;
                            
                            const perguntaLabel = document.createElement('label');
                            perguntaLabel.htmlFor = `opcao-${detalhe.id}-${idx + 1}`;
                            perguntaLabel.innerText = pergunta;
                            
                            checkboxRow.appendChild(checkbox);
                            checkboxRow.appendChild(perguntaLabel);
                            containerOpcoes.appendChild(checkboxRow);
                        });
                        
                        containerPrincipal.appendChild(containerOpcoes);
                        
                        // Botão para salvar as alterações
                        const btnSalvar = document.createElement('button');
                        btnSalvar.className = 'button';
                        btnSalvar.innerText = 'Salvar';
                        btnSalvar.onclick = function() {
                            // Coletando os valores
                            const servicoValue = document.getElementById(`servico-${detalhe.id}`).value;
                            const equipamentoValue = document.getElementById(`equipamento-${detalhe.id}`).value;
                            const executanteValue = document.getElementById(`executante-${detalhe.id}`).value;
                            const operadorValue = document.getElementById(`operador-${detalhe.id}`).value;
                            const smsValue = document.getElementById(`sms-${detalhe.id}`).value;
                            const perigoValue = document.getElementById(`perigo-${detalhe.id}`).value;
                            
                            // Coletando os estados dos checkboxes
                            const checkboxesValues = {};
                            perguntas.forEach((_, idx) => {
                                const checkboxId = `opcao-${detalhe.id}-${idx + 1}`;
                                checkboxesValues[`opcao_${idx + 1}`] = document.getElementById(checkboxId).checked;
                            });
                            
                            // Enviando os dados para o servidor
                            fetch('/salvar_alteracoes', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    id: detalhe.id,
                                    servico: servicoValue,
                                    equipamento: equipamentoValue,
                                    executante: executanteValue,
                                    operador: operadorValue,
                                    sms: smsValue,
                                    perigo: perigoValue,
                                    checkboxes: checkboxesValues
                                })
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    alert('Alterações salvas com sucesso!');
                                } else {
                                    alert('Erro ao salvar alterações: ' + data.message);
                                }
                            })
                            .catch(error => {
                                console.error('Erro:', error);
                                alert('Erro ao salvar alterações.');
                            });
                        };
                        containerPrincipal.appendChild(btnSalvar);
                        
                        resultadoDiv.appendChild(containerPrincipal);
                        resultadoDiv.appendChild(document.createElement('hr'));
                    });
                } else {
                    const noDataText = document.createElement('p');
                    noDataText.innerText = `Nenhum detalhe encontrado para a Especialidade ${especialidade} e Número A.R. ${numero_ar}.`;
                    resultadoDiv.appendChild(noDataText);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar detalhes de elaboração:', error);
            });
        }
        
        // Inicialização quando o arquivo é carregado
        document.getElementById('planilha').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('planilha', file);
                
                                fetch('/carregar_planilha', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = data.message;
                    if (data.success) {
                        carregarEspecialidades();
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('status').innerText = 'Erro ao carregar o arquivo.';
                });
            }
        });
        
        // Executa ao carregar a página
        atualizarUnidade();
        
        // Carregar credenciais salvas, se existirem
        fetch('/carregar_credenciais')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.usuario) document.getElementById('usuario').value = data.usuario;
                if (data.empresa) document.getElementById('empresa').value = data.empresa;
                if (data.area) {
                    document.getElementById('area').value = data.area;
                    atualizarUnidade();
                }
                if (data.unidade) {
                    if (data.area === 'GAS NATURAL&ENERGIA') {
                        document.getElementById('unidadeGas').value = data.unidade;
                    } else {
                        document.getElementById('unidadeRef').value = data.unidade;
                    }
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar credenciais:', error);
        });
    </script>
</body>
</html>
"""

# Criar arquivo HTML
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Rotas da aplicação Flask
"""@app.route('/')
def index():
    return render_template('index.html')"""

"""@app.route('/processar_form', methods=['POST'])
def processar_form():
    global usuario, senha, data, caminho_arquivo
    
    if 'planilha' in request.files:
        arquivo = request.files['planilha']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            os.makedirs('uploads', exist_ok=True)
            arquivo.save(caminho_arquivo)
    
    usuario = request.form.get('usuario', '')
    senha = request.form.get('senha', '')
    data = request.form.get('data', '')
    
    action = request.form.get('action', '')
    
    try:
        if action == 'elaborar_pts':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidadeGas', '')
            else:
                unidade_selecionada = request.form.get('unidadeRef', '')
            
            if not usuario or not senha or not data or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            elaborar_pts(usuario, senha, data, caminho_arquivo, empresa_selecionada, area_selecionada, unidade_selecionada)
            return jsonify({
                'success': True,
                'message': f'PTs elaboradas com sucesso para {os.path.basename(caminho_arquivo)}!'
            })
            
        elif action == 'consultar_ar':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidadeGas', '')
            else:
                unidade_selecionada = request.form.get('unidadeRef', '')
            
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            consultar_ar(usuario, senha, caminho_arquivo, empresa_selecionada, area_selecionada, unidade_selecionada)
            return jsonify({
                'success': True,
                'message': f'Consultando ARs para {usuario}...'
            })
            
        elif action == 'elaborar_ar':
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            elaborar_ar(usuario, senha, caminho_arquivo)
            return jsonify({
                'success': True,
                'message': f'Elaborando ARs para {usuario}...'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro: {str(e)}'
        })
    
    return jsonify({
        'success': True,
        'message': 'Formulário processado com sucesso!'
    })"""
@app.route('/css')
def css():
    return app.send_static_file('style.css')

@app.route('/carregar_planilha', methods=['POST'])
def carregar_planilha():
    global df, especialidades, caminho_arquivo
    
    if 'planilha' in request.files:
        arquivo = request.files['planilha']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            os.makedirs('uploads', exist_ok=True)
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            arquivo.save(caminho_arquivo)
            
            try:
                # Lê o arquivo Excel
                df = pd.read_excel(caminho_arquivo)
                
                if "ESPECIALIDADES" in df.columns:
                    especialidades = sorted(df["ESPECIALIDADES"].dropna().astype(str).unique())
                    return jsonify({
                        'success': True,
                        'message': 'Arquivo carregado com sucesso!'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': "A coluna 'ESPECIALIDADES' não foi encontrada."
                    })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro ao carregar o arquivo: {str(e)}'
                })
    
    return jsonify({
        'success': False,
        'message': 'Nenhum arquivo foi selecionado.'
    })

@app.route('/especialidades')
def get_especialidades():
    if especialidades:
        return jsonify({
            'success': True,
            'especialidades': especialidades
        })
    else:
        return jsonify({
            'success': False,
            'especialidades': [],
            'message': 'Nenhuma especialidade encontrada. Carregue um arquivo Excel primeiro.'
        })

@app.route('/ordens/<especialidade>')
def get_ordens(especialidade):
    if df is not None:
        dados_filtrados = df[df["ESPECIALIDADES"] == especialidade]
        ordens = sorted(dados_filtrados["Ordem"].dropna().unique())
        return jsonify({
            'success': True,
            'ordens': [str(ordem) for ordem in ordens]
        })
    else:
        return jsonify({
            'success': False,
            'ordens': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/detalhes/<especialidade>/<ordem>')
def get_detalhes(especialidade, ordem):
    if df is not None:
        dados_filtrados = df[(df["ESPECIALIDADES"] == especialidade) & (df["Ordem"].astype(str) == ordem)]
        detalhes = []
        
        for _, linha in dados_filtrados.iterrows():
            detalhe = {
                'ordem': str(linha['Ordem']),
                'descricao': str(linha.get('Descrição da PT', '')),
                'libra': str(linha.get('LIBRA', '')),
                'aro': str(linha.get('ARO', '')),
                'ar': str(linha.get('Número\nA.R.', ''))
            }
            detalhes.append(detalhe)
        
        return jsonify({
            'success': True,
            'detalhes': detalhes
        })
    else:
        return jsonify({
            'success': False,
            'detalhes': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/analises_pendentes/<especialidade>')
def get_analises_pendentes(especialidade):
    if df is not None:
        dados_filtrados = df[df["ESPECIALIDADES"] == especialidade]
        numeros_ar = sorted(dados_filtrados["Número\nA.R."].dropna().astype(str).unique())
        return jsonify({
            'success': True,
            'numeros_ar': numeros_ar
        })
    else:
        return jsonify({
            'success': False,
            'numeros_ar': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/detalhes_elaboracao/<especialidade>/<numero_ar>')
def get_detalhes_elaboracao(especialidade, numero_ar):
    if df is not None:
        dados_filtrados = df[(df["ESPECIALIDADES"] == especialidade) & (df["Número\nA.R."].astype(str) == numero_ar)]
        detalhes = []
        
        for idx, linha in dados_filtrados.iterrows():
            detalhe = {
                'id': idx,
                'numero_ar': str(linha.get('Número\nA.R.', '')),
                'ordem': str(linha.get('Ordem', '')),
                'servico': str(linha.get('Serviço', '')),
                'equipamento': str(linha.get('Equipamento', '')),
                'executante': str(linha.get('Executante', '')),
                'operador': str(linha.get('Operador', '')),
                'sms': str(linha.get('SMS', '')),
                'perigo': str(linha.get('Perigo', ''))
            }
            
            # Adicionar estados dos checkboxes
            for i in range(1, 10):  # 9 perguntas
                detalhe[f'opcao_{i}'] = bool(linha.get(f'Opção {i}', False))
            
            detalhes.append(detalhe)
        
        return jsonify({
            'success': True,
            'detalhes': detalhes
        })
    else:
        return jsonify({
            'success': False,
            'detalhes': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/salvar_alteracoes', methods=['POST'])
def salvar_alteracoes():
    global df
    
    if df is None:
        return jsonify({
            'success': False,
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })
    
    data = request.json
    if not data:
        return jsonify({
            'success': False,
            'message': 'Dados não recebidos.'
        })
    
    try:
        idx = data.get('id')
        
        # Atualiza os valores no DataFrame
        df.at[idx, 'Serviço'] = data.get('servico', '')
        df.at[idx, 'Equipamento'] = data.get('equipamento', '')
        df.at[idx, 'Executante'] = data.get('executante', '')
        df.at[idx, 'Operador'] = data.get('operador', '')
        df.at[idx, 'SMS'] = data.get('sms', '')
        df.at[idx, 'Perigo'] = data.get('perigo', '')
        
        # Atualiza os checkboxes
        checkboxes = data.get('checkboxes', {})
        for key, value in checkboxes.items():
            # Converte 'opcao_1' para 'Opção 1'
            coluna = key.replace('opcao_', 'Opção ')
            df.at[idx, coluna] = value
        
        # Opcional: salvar o DataFrame atualizado no arquivo
        if caminho_arquivo:
            df.to_excel(caminho_arquivo, index=False)
        
        return jsonify({
            'success': True,
            'message': 'Alterações salvas com sucesso!'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao salvar alterações: {str(e)}'
        })

@app.route('/carregar_credenciais')
def carregar_credenciais():
    try:
        if os.path.exists('credentials.json'):
            with open('credentials.json', 'r', encoding='utf-8') as f:
                credentials = json.load(f)
            
            # Não enviar a senha por segurança
            if 'senha' in credentials:
                del credentials['senha']
                
            return jsonify({
                'success': True,
                **credentials
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Arquivo de credenciais não encontrado.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar credenciais: {str(e)}'
        })
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # Aqui você adicionaria a lógica para validar as credenciais
            # Por enquanto, apenas simulamos um login bem-sucedido
            session['username'] = username
            session['unidade'] = 'UTE-NPI'  # Exemplo
            return redirect(url_for('dashboard'))
        else:
            error = 'Usuário ou senha inválidos'
    return render_template('login.html', error=error, current_year=datetime.datetime.now().year)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    # Dados de exemplo para o dashboard
    stats = {
        'pts_total': 120,
        'pts_emitidas': 85,
        'pts_pendentes': 30,
        'ars_total': 95
    }
    
    activities = [
        {
            'icon': '📄',
            'title': 'PT Emitida',
            'description': 'PT #12345 foi emitida com sucesso',
            'time': 'Há 10 minutos'
        },
        {
            'icon': '⚠️',
            'title': 'AR Pendente',
            'description': 'AR para ordem #67890 precisa ser elaborada',
            'time': 'Há 30 minutos'
        },
        # Adicione mais atividades conforme necessário
    ]
    
    upcoming_pts = [
        {
            'ordem': '12345',
            'descricao': 'Manutenção Preventiva UG-01',
            'data': '12/11/2023',
            'status': 'Emitida'
        },
        {
            'ordem': '67890',
            'descricao': 'Inspeção de Válvulas',
            'data': '13/11/2023',
            'status': 'Pendente'
        },
        # Adicione mais PTs conforme necessário
    ]
    
    return render_template(
        'dashboard.html', 
        active_page='dashboard',
        stats=stats,
        activities=activities,
        upcoming_pts=upcoming_pts,
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[]  # Dashboard não precisa de breadcrumb
    )

@app.route('/elaborar_pts')
def elaborar_pts_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'elaborar_pts.html', 
        active_page='elaborar_pts',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Elaborar PTs', 'url': '#'}
        ]
    )

@app.route('/consultar_ar')
def consultar_ar_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'consultar_ar.html', 
        active_page='consultar_ar',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Consultar ARs', 'url': '#'}
        ]
    )
    
@app.route('/resultado')
def resultado_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    # Dados de exemplo para os resultados
    stats = {
        'pts_emitidas': 25,
        'pts_pendentes': 5,
        'erros': 2,
        'tempo_total': '15:30 min'
    }
    
    resultados = [
        {
            'ordem': '12345',
            'descricao': 'Manutenção Preventiva UG-01',
            'numero_pt': 'PT-2023-12345',
            'numero_ar': 'AR-2023-5678',
            'data': '12/11/2023',
            'status': 'Emitida'
        },
        {
            'ordem': '67890',
            'descricao': 'Inspeção de Válvulas',
            'numero_pt': None,
            'numero_ar': 'AR-2023-9012',
            'data': '13/11/2023',
            'status': 'Pendente'
        },
        {
            'ordem': '54321',
            'descricao': 'Troca de Filtros',
            'numero_pt': None,
            'numero_ar': None,
            'data': '14/11/2023',
            'status': 'Erro'
        },
        # Adicione mais resultados conforme necessário
    ]
    
    return render_template(
        'resultado.html', 
        active_page='elaborar_pts',  # Mantém ativo o menu de elaborar PTs
        stats=stats,
        resultados=resultados,
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Elaborar PTs', 'url': url_for('elaborar_pts_page')},
            {'label': 'Resultados', 'url': '#'}
        ]
    )

@app.route('/relatorios')
def relatorios_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'relatorios.html', 
        active_page='relatorios',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Relatórios', 'url': '#'}
        ]
    )

@app.route('/historico')
def historico_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'historico.html', 
        active_page='historico',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Histórico', 'url': '#'}
        ]
    )

@app.route('/configuracoes')
def configuracoes_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'configuracoes.html', 
        active_page='configuracoes',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Configurações', 'url': '#'}
        ]
    )

# Rotas para API e processamento de formulários

@app.route('/processar_form', methods=['POST'])
def processar_form():
    global usuario, senha, data, caminho_arquivo
    
    # Processar arquivo se enviado
    if 'planilha' in request.files:
        arquivo = request.files['planilha']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            os.makedirs('uploads', exist_ok=True)
            arquivo.save(caminho_arquivo)
    elif 'arquivo' in request.files:  # Suporte para outro nome de campo de arquivo
        arquivo = request.files['arquivo']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            os.makedirs('uploads', exist_ok=True)
            arquivo.save(caminho_arquivo)
    
    # Obter parâmetros do formulário
    usuario = request.form.get('usuario', '')
    senha = request.form.get('senha', '')
    data = request.form.get('data', '')
    action = request.form.get('action', '')
    
    try:
        if action == 'elaborar_pts':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidade', '')
            else:
                unidade_selecionada = request.form.get('unidade', '')
            
            if not usuario or not senha or not data or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # IMPORTANTE: Aqui chamamos a função elaborar_pts diretamente
            # Isso garante que ela seja chamada independentemente do tipo de resposta
            try:
                # Inicie a função em uma thread separada para não bloquear a resposta
                import threading
                
                def run_elaboration():
                    try:
                        elaborar_pts(usuario, senha, data, caminho_arquivo, 
                                    empresa_selecionada, area_selecionada, unidade_selecionada)
                        print("Elaboração de PTs concluída com sucesso!")
                    except Exception as e:
                        print(f"Erro durante a elaboração de PTs: {str(e)}")
                
                # Inicia a thread para executar a elaboração em segundo plano
                thread = threading.Thread(target=run_elaboration)
                thread.daemon = True
                thread.start()
                
                # Agora podemos responder imediatamente enquanto a elaboração continua em segundo plano
                return jsonify({
                    'success': True,
                    'message': f'Elaborando PTs para {os.path.basename(caminho_arquivo)}...',
                    'redirect': '/resultado'
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro ao iniciar elaboração: {str(e)}'
                })
        
        elif action == 'consultar_ar':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidadeGas', '')
            else:
                unidade_selecionada = request.form.get('unidadeRef', '')
            
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            try:
                consultar_ar(usuario, senha, caminho_arquivo, empresa_selecionada, 
                            area_selecionada, unidade_selecionada)
                return jsonify({
                    'success': True,
                    'message': f'Consultando ARs para {usuario}...'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro na consulta de AR: {str(e)}'
                })
        
        elif action == 'elaborar_ar':
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            try:
                elaborar_ar(usuario, senha, caminho_arquivo)
                return jsonify({
                    'success': True,
                    'message': f'Elaborando ARs para {usuario}...'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro na elaboração de AR: {str(e)}'
                })
        
        else:
            return jsonify({
                'success': False,
                'message': 'Ação desconhecida'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro geral: {str(e)}'
        })

@app.route('/detalhes_pt/<ordem>')
def detalhes_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
        # Simulação de dados da PT
    pt_data = {
        'ordem': ordem,
        'numero_pt': f'PT-2023-{ordem}',
        'numero_ar': f'AR-2023-{int(ordem) % 10000}',
        'data': '12/11/2023',
        'status': 'Emitida',
        'descricao': 'Manutenção preventiva nos equipamentos da unidade geradora.',
        'recomendacoes': 'Utilizar EPI adequado. Verificar isolamento da área. Comunicar operação antes do início das atividades.'
    }
    
    return jsonify(pt_data)

@app.route('/imprimir_pt/<ordem>')
def imprimir_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Aqui você implementaria a geração do PDF para impressão
    # Por enquanto, apenas retorna uma mensagem
    response = make_response("Simulação de PDF da PT")
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=PT-{ordem}.pdf"
    return response

@app.route('/reprocessar_pt/<ordem>', methods=['POST'])
def reprocessar_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Simulação de reprocessamento
    time.sleep(2)  # Simula processamento
    
    # Retorna sucesso
    return jsonify({
        'success': True,
        'message': f'PT para ordem {ordem} reprocessada com sucesso!'
    })

@app.route('/erro_pt/<ordem>')
def erro_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Simulação de dados do erro
    erro_data = {
        'message': 'Não foi possível conectar ao sistema SPT.',
        'timestamp': '12/11/2023 14:35:22',
        'log': 'Error: Connection timeout after 30000ms\nAttempting to reconnect...\nFailed to reconnect: Server unavailable',
        'suggestions': [
            'Verifique sua conexão com a rede corporativa.',
            'Tente novamente em alguns minutos.',
            'Se o problema persistir, entre em contato com o suporte.'
        ]
    }
    
    return jsonify(erro_data)

@app.route('/exportar_excel')
def exportar_excel():
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Aqui você implementaria a geração do Excel
    # Por enquanto, apenas retorna uma mensagem
    response = make_response("Simulação de arquivo Excel")
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=resultados_pts.xlsx"
    return response

# Rota raiz - redireciona para login ou dashboard
@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# Função para iniciar o navegador automaticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Definir função principal
def main():
    # Iniciar o navegador automaticamente quando o servidor iniciar
    threading.Timer(1.5, open_browser).start()
    
    # Iniciar o servidor Flask
    app.run(debug=True)

if __name__ == "__main__":
=======
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, Response, make_response
import time
import json
import datetime
import os
from werkzeug.utils import secure_filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import numpy as np
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import filedialog, messagebox
import flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
import webbrowser
import json

# Importações do módulo elaborador (assumindo que o módulo existe)
from elaborador import (
    elaborar_pts,
    consultar_ar,
    elaborar_ar,
)

# Variáveis globais
usuario = ""
senha = ""
data = ""
caminho_arquivo = ""
df = None  # DataFrame global
especialidades = []  # Lista global para armazenar as especialidades únicas

# Criar aplicação Flask
app = Flask(__name__)
app.secret_key = 'J0@0P@uloFla'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.static_folder = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Garante que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configurar pasta de templates
app.template_folder = 'templates'

# Configurar pasta de arquivos estáticos
app.static_folder = 'static'

# Criar pasta de templates se não existir
if not os.path.exists('templates'):
    os.makedirs('templates')

# Criar pasta de arquivos estáticos se não existir
if not os.path.exists('static'):
    os.makedirs('static')

# Criar arquivo CSS básico
css_content = """
:root {
  --petrobras-green: #009846;
  --petrobras-green-dark: #006633;
  --petrobras-yellow: #FCCE03;
  --petrobras-blue: #0064AF;
  --petrobras-gray: #58595B;
  --petrobras-light-gray: #F2F2F2;
}
body {
  font-family: 'Open Sans', Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: var(--petrobras-light-gray);
  color: #333;
}
.container {
    display: flex;
    flex-wrap: wrap;
    padding: 20px;
    gap: 20px;
    max-width: 1400px;
    margin: 0 auto;
}
.sidebar {
    flex: 1;
    min-width: 300px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 20px;
}
.content {
    flex: 3;
    display: flex;
    flex-direction: column;
    min-width: 600px;
}
/* Responsividade */
@media (max-width: 992px) {
  .container {
    flex-direction: column;
  }
  
  .sidebar, .content {
    min-width: 100%;
  }
}
.tabs {
    display: flex;
    margin-bottom: 10px;
}
.tab {
    padding: 10px 20px;
    background-color: #ddd;
    border: none;
    cursor: pointer;
    margin-right: 5px;
    border-radius: 5px 5px 0 0;
}
.tab.active {
    background-color: #fff;
}
.tab-content {
    display: flex;
    flex: 1;
}
.gallery {
    flex: 1;
    background-color: #e0e0e0;
    padding: 10px;
    border-radius: 5px;
    margin-right: 10px;
    overflow-y: auto;
    max-height: 600px;
}
.result {
    flex: 2;
    background-color: #d0d0d0;
    padding: 10px;
    border-radius: 5px;
    overflow-y: auto;
    max-height: 600px;
}
.button {
    background-color: var(--petrobras-green);
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
}
.button:hover {
  background-color: var(--petrobras-green-dark);
}
.button-blue {
    background-color: var(--petrobras-blue);
}
.button-orange {
    background-color: var(--petrobras-yellow);
    color: #333;
}
.header {
    background-color: var(--petrobras-green);
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header img {
    height: 90px;
}
.text-button {
    background: none;
    border: none;
    color: #2196F3;
    padding: 5px;
    text-align: left;
    text-decoration: underline;
    display: block;
    font-size: 16px;
    margin: 2px 0;
    cursor: pointer;
}
input[type=text], input[type=password], input[type=date], select {
  width: 100%;
  padding: 12px;
  margin: 8px 0 16px;
  display: block;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 16px;
  transition: border-color 0.3s;
}
input[type=text]:focus, input[type=password]:focus, input[type=date]:focus, select:focus {
  border-color: var(--petrobras-green);
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 152, 70, 0.2);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
  color: var(--petrobras-gray);
}

.form-control {
  position: relative;
}

.form-control .icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--petrobras-gray);
}

.file-input-wrapper {
  position: relative;
  overflow: hidden;
  display: inline-block;
  margin: 15px 0;
}

.file-input-wrapper input[type=file] {
  position: absolute;
  font-size: 100px;
  opacity: 0;
  right: 0;
  top: 0;
  cursor: pointer;
}

.file-input-button {
  display: inline-block;
  background-color: var(--petrobras-blue);
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.file-name {
  margin-left: 10px;
  font-style: italic;
}
/* Adicione ao style.css */
.tabs {
  display: flex;
  background-color: white;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  margin-bottom: 0;
  box-shadow: 0 -2px 4px rgba(0,0,0,0.05);
}

.tab {
  padding: 15px 25px;
  background-color: white;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: var(--petrobras-gray);
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
}

.tab.active {
  color: var(--petrobras-green);
  border-bottom: 3px solid var(--petrobras-green);
}

.tab:hover:not(.active) {
  background-color: #f9f9f9;
  color: #333;
}

.tab-content {
  background-color: white;
  border-radius: 0 0 8px 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  flex: 1;
  gap: 20px;
}
/* Adicione ao style.css */
.gallery, .result {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  overflow-y: auto;
  max-height: 600px;
}

.gallery {
  flex: 1;
  border-left: 4px solid var(--petrobras-blue);
}

.result {
  flex: 2;
  border-left: 4px solid var(--petrobras-green);
}

.text-button {
  background: none;
  border: none;
  color: var(--petrobras-blue);
  padding: 8px 12px;
  text-align: left;
  display: block;
  font-size: 15px;
  margin: 2px 0;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
  width: 100%;
}

.text-button:hover {
  background-color: rgba(0, 100, 175, 0.1);
}

.data-card {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 15px;
  border-left: 4px solid var(--petrobras-green);
}

.data-card h3 {
  margin-top: 0;
  color: var(--petrobras-gray);
  font-size: 18px;
}

.data-card p {
  margin: 8px 0;
  font-size: 14px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.status-emitida {
  background-color: var(--petrobras-green);
  color: white;
}

.status-elaborar {
  background-color: var(--petrobras-yellow);
  color: #333;
}

.status-erro {
  background-color: #e74c3c;
  color: white;
}

/* Tabela de resultados */
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
}

.data-table th {
  background-color: var(--petrobras-light-gray);
  color: var(--petrobras-gray);
  font-weight: 600;
  text-align: left;
  padding: 12px 15px;
}

.data-table td {
  border-bottom: 1px solid #eee;
  padding: 10px 15px;
}

.data-table tr:hover {
  background-color: rgba(0, 152, 70, 0.05);
}

.data-table .actions {
  display: flex;
  gap: 8px;
}

.data-table .action-button {
  background: none;
  border: none;
  color: var(--petrobras-blue);
  cursor: pointer;
  font-size: 16px;
}

.data-table .action-button:hover {
  color: var(--petrobras-green);
}

.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-actions {
  display: flex;
  gap: 10px;
}

.dashboard-stats {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 200px;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 28px;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--petrobras-green);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--petrobras-gray);
  font-size: 14px;
}

.dashboard-content {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.recent-activities, .upcoming-tasks {
  flex: 1;
  min-width: 300px;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.activity-list {
  margin-top: 15px;
}

.activity-item {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.activity-icon {
  width: 40px;
  height: 40px;
  background-color: var(--petrobras-light-gray);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 18px;
}

.activity-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.activity-desc {
  font-size: 14px;
  color: var(--petrobras-gray);
}

.activity-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.loader-overlay.active {
  opacity: 1;
  visibility: visible;
}

.loader-container {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  max-width: 80%;
  width: 400px;
}

.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid var(--petrobras-green);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loader-text {
  font-size: 18px;
  margin-bottom: 15px;
  color: var(--petrobras-gray);
}

.loader-progress-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--petrobras-green);
  margin-bottom: 10px;
}

.loader-progress-bar {
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  overflow: hidden;
}

.loader-progress-fill {
  height: 100%;
  background-color: var(--petrobras-green);
  width: 0%;
  transition: width 0.3s ease-in-out;
}
/* Adicione ao style.css */
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 300px;
  z-index: 1000;
}

.notification {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16);
  animation: slide-in 0.3s ease-out forwards;
  position: relative;
  display: flex;
  align-items: flex-start;
}

.notification-success {
  background-color: #d4edda;
  border-left: 4px solid var(--petrobras-green);
  color: #155724;
}

.notification-error {
  background-color: #f8d7da;
  border-left: 4px solid #dc3545;
  color: #721c24;
}

.notification-warning {
  background-color: #fff3cd;
  border-left: 4px solid var(--petrobras-yellow);
  color: #856404;
}

.notification-info {
  background-color: #d1ecf1;
  border-left: 4px solid var(--petrobras-blue);
  color: #0c5460;
}

.notification-icon {
  margin-right: 10px;
  font-size: 20px;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.notification-message {
  font-size: 14px;
}

.notification-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 18px;
  opacity: 0.5;
  padding: 0;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fade-out {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}
/* Adicione ao style.css */
.results-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-actions {
  display: flex;
  gap: 10px;
}

.results-summary {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.summary-card {
  flex: 1;
  min-width: 200px;
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
}

.summary-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
}

.summary-icon.success {
  background-color: rgba(0, 152, 70, 0.1);
  color: var(--petrobras-green);
}

.summary-icon.warning {
  background-color: rgba(252, 206, 3, 0.1);
  color: #856404;
}

.summary-icon.error {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.summary-icon.info {
  background-color: rgba(0, 100, 175, 0.1);
  color: var(--petrobras-blue);
}

.summary-content {
  flex: 1;
}

.summary-title {
  font-size: 14px;
  color: var(--petrobras-gray);
  margin-bottom: 5px;
}

.summary-number {
  font-size: 24px;
  font-weight: 700;
}

.results-filter {
  display: flex;
  gap: 20px;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group label {
  font-weight: 600;
  color: var(--petrobras-gray);
  white-space: nowrap;
}

.filter-group select, .filter-group input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.results-table-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

.results-table {
  margin: 0;
}

.results-table td {
  vertical-align: middle;
}

.no-results {
  padding: 40px;
  text-align: center;
  color: var(--petrobras-gray);
}

.no-results i {
  font-size: 48px;
  margin-bottom: 15px;
  color: #ddd;
}

.no-results h3 {
  margin-bottom: 10px;
}

.no-results p {
  max-width: 400px;
  margin: 0 auto;
}
/* Estilos para os detalhes da PT e erros */
.pt-details, .error-details {
  width: 100%;
}

.details-section, .error-section {
  margin-bottom: 20px;
}

.details-section h4, .error-section h4 {
  color: var(--petrobras-green);
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
  margin-top: 0;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 12px;
  color: var(--petrobras-gray);
  margin-bottom: 5px;
}

.detail-value {
  font-weight: 600;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 10px;
  font-weight: 600;
}

.error-timestamp {
  font-size: 12px;
  color: var(--petrobras-gray);
  text-align: right;
}

.error-log {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  max-height: 200px;
  overflow-y: auto;
  font-size: 12px;
}

.error-suggestions li {
  margin-bottom: 8px;
}
/* Adicione ao style.css */
.main-container {
  display: flex;
  min-height: calc(100vh - 70px);
}

.sidebar {
  width: 250px;
  background-color: white;
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.nav-menu {
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: var(--petrobras-gray);
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: rgba(0, 152, 70, 0.05);
  color: var(--petrobras-green);
}

.nav-item.active {
  background-color: rgba(0, 152, 70, 0.1);
  color: var(--petrobras-green);
  border-left-color: var(--petrobras-green);
  font-weight: 600;
}

.nav-item i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.sidebar-info {
  margin-top: auto;
  padding: 20px;
  border-top: 1px solid #eee;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  color: var(--petrobras-gray);
  font-size: 14px;
}

.info-item i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: var(--petrobras-light-gray);
  overflow-x: hidden;
}

.breadcrumb {
  background-color: white;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  font-size: 14px;
}

.breadcrumb a {
  color: var(--petrobras-blue);
  text-decoration: none;
}

.breadcrumb-separator {
  margin: 0 10px;
  color: #ccc;
}

.breadcrumb-current {
  color: var(--petrobras-gray);
  font-weight: 600;
}

.content {
  flex: 1;
}

.footer {
  margin-top: 30px;
  padding: 15px 0;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  color: var(--petrobras-gray);
  font-size: 14px;
}

.logout-btn {
  margin-left: 15px;
  color: #dc3545;
  text-decoration: none;
  font-size: 14px;
}

.logout-btn:hover {
  text-decoration: underline;
}

/* Responsividade */
@media (max-width: 992px) {
  .main-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .nav-menu {
    display: flex;
    overflow-x: auto;
    padding: 10px;
  }
  
  .nav-item {
    padding: 10px 15px;
    border-left: none;
    border-bottom: 3px solid transparent;
    white-space: nowrap;
  }
  
  .nav-item.active {
    border-left-color: transparent;
    border-bottom-color: var(--petrobras-green);
  }
  
  .sidebar-info {
    display: none;
  }
  
  .header {
    flex-direction: column;
    text-align: center;
    padding: 10px;
  }
  
  .header-title h1 {
    font-size: 18px;
    margin: 10px 0;
  }
  
  .user-info {
    margin-top: 10px;
  }
}
/* Adicione ao style.css */
.login-page {
  background-color: var(--petrobras-light-gray);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 1000px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-header {
  background-color: var(--petrobras-green);
  color: white;
  padding: 20px;
  text-align: center;
}

.login-logo {
  height: 60px;
  margin-bottom: 15px;
}

.login-header h1 {
  font-size: 24px;
  margin: 0;
  font-weight: 600;
}

.login-form-container {
  display: flex;
}

.login-form-wrapper {
  flex: 1;
  padding: 30px;
  border-right: 1px solid #eee;
}

.login-form-wrapper h2 {
  color: var(--petrobras-green);
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 22px;
}

.login-info {
  flex: 1;
  padding: 30px;
  background-color: #f9f9f9;
}

.info-box {
  margin-bottom: 30px;
}

.info-box h3 {
  color: var(--petrobras-blue);
  font-size: 18px;
  margin-top: 0;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.info-box h3 i {
  margin-right: 10px;
}

.info-box p {
  color: var(--petrobras-gray);
  margin-bottom: 10px;
  line-height: 1.5;
}

.info-box ul {
  padding-left: 20px;
  color: var(--petrobras-gray);
}

.info-box li {
  margin-bottom: 8px;
}

.info-box li i {
  margin-right: 10px;
  color: var(--petrobras-blue);
}

.login-footer {
  background-color: #f2f2f2;
  padding: 15px;
  text-align: center;
  border-top: 1px solid #eee;
  color: var(--petrobras-gray);
  font-size: 14px;
}

.login-footer p {
  margin: 5px 0;
}

.login-error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px 15px;
  border-radius: 4px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.login-error i {
  margin-right: 10px;
  font-size: 18px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.remember-me {
  display: flex;
  align-items: center;
}

.remember-me input {
  margin-right: 8px;
}

.forgot-password {
  color: var(--petrobras-blue);
  text-decoration: none;
  font-size: 14px;
}

.forgot-password:hover {
  text-decoration: underline;
}

.button-full {
  width: 100%;
}

/* Responsividade */
@media (max-width: 768px) {
  .login-form-container {
    flex-direction: column;
  }
  
  .login-form-wrapper {
    border-right: none;
    border-bottom: 1px solid #eee;
  }
}
/* Adicione ao style.css */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: var(--petrobras-green);
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--petrobras-gray);
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.modal-footer {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.button-outline {
  background-color: transparent;
  border: 1px solid var(--petrobras-green);
  color: var(--petrobras-green);
}

.button-outline:hover {
  background-color: rgba(0, 152, 70, 0.1);
}
/* Adicione ao style.css */
.page-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.page-header h2 {
  color: var(--petrobras-green);
  margin: 0;
}

.form-container {
  margin-bottom: 30px;
}

.config-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section {
  background-color: #f9f9f9;
  border-radius: 6px;
  padding: 20px;
  border: 1px solid #eee;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: var(--petrobras-gray);
  font-size: 18px;
}

.form-row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 10px;
}

.button-small {
  padding: 5px 10px;
  font-size: 14px;
}

.file-preview {
  margin-top: 15px;
  background-color: white;
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 15px;
}

.file-preview h4 {
  margin-top: 0;
  color: var(--petrobras-gray);
  font-size: 16px;
  margin-bottom: 10px;
}

.preview-info {
  margin-bottom: 15px;
}

.preview-info p {
  margin: 5px 0;
}

.preview-actions {
  text-align: right;
}

.resultado-container {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
  border: 1px solid #eee;
}


.hidden {
    display: none;
}
"""

# Criar arquivo CSS
with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

# Criar arquivo HTML básico
html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acompanhamento de PTs</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="header">
        <div class="logo">
            <img src="{{ url_for('static', filename='logo-petrobras.png') }}" alt="Petrobras">
        </div>
        <div class="header-title">
            <h1>Sistema de Gestão de Permissões de Trabalho</h1>
        </div>
        <div class="user-info">
            <span id="username">Usuário: </span>
        </div>
    </div>

    <div class="container">
        <div class="sidebar">
            <h2>Informações</h2>
            <form id="configForm" method="post" enctype="multipart/form-data" action="{{ url_for('processar_form') }}">
                <label for="usuario">Usuário:</label>
                <input type="text" id="usuario" name="usuario" required>
                
                <label for="senha">Senha:</label>
                <input type="password" id="senha" name="senha" required>
                
                <label for="empresa">Empresa:</label>
                <select id="empresa" name="empresa">
                    <option value="PETROBRAS">PETROBRAS</option>
                </select>
                
                <label for="area">Área ou Gerência:</label>
                <select id="area" name="area" onchange="atualizarUnidade()">
                    <option value="GAS NATURAL&ENERGIA">GAS NATURAL&ENERGIA</option>
                    <option value="REFINO">REFINO</option>
                </select>
                
                <div id="unidadeGasNatural">
                    <label for="unidadeGas">Unidade:</label>
                    <select id="unidadeGas" name="unidadeGas">
                        <option value="UTE-BF">UTE-BF</option>
                        <option value="UTE-CAN">UTE-CAN</option>
                        <option value="UTE-CBT">UTE-CBT</option>
                        <option value="UTE-IBT">UTE-IBT</option>
                        <option value="UTE-JF">UTE-JF</option>
                        <option value="UTE-NPI">UTE-NPI</option>
                        <option value="UTE-SRP">UTE-SRP</option>
                        <option value="UTE-TBA-TCA">UTE-TBA-TCA</option>
                        <option value="UTE-TCE">UTE-TCE</option>
                        <option value="UTE-TLG">UTE-TLG</option>
                        <option value="UTE-TMA">UTE-TMA</option>
                        <option value="UTE-TRI">UTE-TRI</option>
                        <option value="UTE-VLA">UTE-VLA</option>
                        <option value="UTGC e UTGSUL">UTGC e UTGSUL</option>
                        <option value="UTGCA">UTGCA</option>
                        <option value="UTGCAB">UTGCAB</option>
                        <option value="UTGITB">UTGITB</option>
                    </select>
                </div>
                
                <div id="unidadeRefino" class="hidden">
                    <label for="unidadeRef">Unidade:</label>
                    <select id="unidadeRef" name="unidadeRef">
                        <option value="FAFEN-BA">FAFEN-BA</option>
                        <option value="FAFEN-SE">FAFEN-SE</option>
                        <option value="LUBNOR">LUBNOR</option>
                        <option value="PROTEGE+">PROTEGE+</option>
                        <option value="RECAP">RECAP</option>
                        <option value="REDUC">REDUC</option>
                        <option value="REFAP">REFAP</option>
                        <option value="REGAP">REGAP</option>
                        <option value="REMAN">REMAN</option>
                        <option value="REPAR">REPAR</option>
                        <option value="REPLAN">REPLAN</option>
                        <option value="REVAP">REVAP</option>
                        <option value="RLAM">RLAM</option>
                        <option value="RNEST">RNEST</option>
                        <option value="RPBC">RPBC</option>
                        <option value="SIX">SIX</option>
                    </select>
                </div>
                
                <label for="data">Data para emissão:</label>
                <input type="date" id="data" name="data">
                
                <input type="file" id="planilha" name="planilha" accept=".xlsx,.xls">
                
                <div id="status"></div>
                
                <div>
                    <button type="button" class="button" onclick="elaborarPTs()">Elaborar PTs</button>
                    <button type="button" class="button button-blue" onclick="consultarAR()">Consultar AR</button>
                    <button type="button" class="button button-orange" onclick="elaborarAR()">Elaborar AR</button>
                </div>
                
                <div id="resultado"></div>
            </form>
        </div>
        
        <div class="content">
            <div class="tabs">
                <button class="tab active" onclick="showTab('acompanhamento')">Acompanhamento da Programação</button>
                <button class="tab" onclick="showTab('elaboracao')">Elaboração de AR</button>
            </div>
            
            <div id="acompanhamento" class="tab-content">
                <div class="gallery" id="galeria">
                    <!-- Especialidades serão carregadas aqui -->
                </div>
                <div class="result" id="resultado-acompanhamento">
                    <!-- Resultados serão exibidos aqui -->
                </div>
            </div>
            
            <div id="elaboracao" class="tab-content hidden">
                <div class="gallery" id="galeria-elaboracao">
                    <!-- Especialidades serão carregadas aqui para elaboração -->
                </div>
                <div class="result" id="resultado-elaboracao">
                    <!-- Resultados de elaboração serão exibidos aqui -->
                </div>
            </div>
        </div>
    </div>
    <div id="loader-overlay" class="loader-overlay">
        <div class="loader-container">
            <div class="loader"></div>
            <div class="loader-text">Processando...</div>
            <div id="loader-progress-text" class="loader-progress-text">0%</div>
            <div class="loader-progress-bar">
            <div id="loader-progress" class="loader-progress-fill"></div>
            </div>
        </div>
    </div>
    <div id="notification-container" class="notification-container"></div>
    <div id="modal-overlay" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3 id="modal-title">Título do Modal</h3>
                <button class="modal-close">&times;</button>
            </div>
            <div class="modal-body" id="modal-body">
                Conteúdo do modal
            </div>
            <div class="modal-footer">
                <button class="button button-outline" id="modal-cancel">Cancelar</button>
                <button class="button" id="modal-confirm">Confirmar</button>
            </div>
        </div>
    </div>
    
    <script>
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
        function voltarDashboard() {
            window.location.href = '/dashboard';
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
                    iconClass = 'ℹ️';
                    break;
                default:
                    iconClass = '?';
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
        function atualizarUnidade() {
            var area = document.getElementById('area').value;
            if (area === 'GAS NATURAL&ENERGIA') {
                document.getElementById('unidadeGasNatural').classList.remove('hidden');
                document.getElementById('unidadeRefino').classList.add('hidden');
            } else {
                document.getElementById('unidadeGasNatural').classList.add('hidden');
                document.getElementById('unidadeRefino').classList.remove('hidden');
            }
        }
        
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

        
        function consultarAR() {
            var formData = new FormData(document.getElementById('configForm'));
            formData.append('action', 'consultar_ar');
            
            fetch('/processar_form', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('resultado').innerText = data.message;
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('resultado').innerText = 'Erro ao processar a solicitação.';
            });
        }
        
        function elaborarAR() {
            var formData = new FormData(document.getElementById('configForm'));
            formData.append('action', 'elaborar_ar');
            
            fetch('/processar_form', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('resultado').innerText = data.message;
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('resultado').innerText = 'Erro ao processar a solicitação.';
            });
        }
        
        function carregarEspecialidades() {
            fetch('/especialidades')
            .then(response => response.json())
            .then(data => {
                const galeriaDiv = document.getElementById('galeria');
                const galeriaElaboracaoDiv = document.getElementById('galeria-elaboracao');
                
                galeriaDiv.innerHTML = '';
                galeriaElaboracaoDiv.innerHTML = '';
                
                data.especialidades.forEach(esp => {
                    // Para aba de acompanhamento
                    const btn = document.createElement('button');
                    btn.className = 'text-button';
                    btn.innerText = esp;
                    btn.onclick = function() { exibirOpcoesOrdem(esp); };
                    galeriaDiv.appendChild(btn);
                    
                    // Para aba de elaboração
                    const btnElab = document.createElement('button');
                    btnElab.className = 'text-button';
                    btnElab.innerText = esp;
                    btnElab.onclick = function() { exibirAnalisesPendentes(esp); };
                    galeriaElaboracaoDiv.appendChild(btnElab);
                });
            })
            .catch(error => {
                console.error('Erro ao carregar especialidades:', error);
            });
        }
        
        function exibirOpcoesOrdem(especialidade) {
            fetch(`/ordens/${especialidade}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-acompanhamento');
                resultadoDiv.innerHTML = '';
                
                data.ordens.forEach(ordem => {
                    const btn = document.createElement('button');
                    btn.className = 'text-button';
                    btn.innerText = `Ordem: ${ordem}`;
                    btn.onclick = function() { mostrarDetalhes(especialidade, ordem); };
                    resultadoDiv.appendChild(btn);
                                });
            })
            .catch(error => {
                console.error('Erro ao carregar ordens:', error);
            });
        }
        
        function mostrarDetalhes(especialidade, ordem) {
            fetch(`/detalhes/${especialidade}/${ordem}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-acompanhamento');
                resultadoDiv.innerHTML = '';
                
                if (data.detalhes.length > 0) {
                    data.detalhes.forEach(detalhe => {
                        // Adiciona a Ordem
                        const ordemText = document.createElement('h3');
                        ordemText.innerText = `Ordem: ${detalhe.ordem}`;
                        resultadoDiv.appendChild(ordemText);
                        
                        // Adiciona a Descrição
                        const descText = document.createElement('p');
                        descText.innerText = `Descrição da PT: ${detalhe.descricao}`;
                        resultadoDiv.appendChild(descText);
                        
                        // Adiciona LIBRA, ARO e AR
                        const infoText = document.createElement('p');
                        infoText.innerText = `LIBRA: ${detalhe.libra}, ARO: ${detalhe.aro}, Análise de Risco: ${detalhe.ar}`;
                        resultadoDiv.appendChild(infoText);
                        
                        // Separador
                        const divider = document.createElement('hr');
                        resultadoDiv.appendChild(divider);
                    });
                } else {
                    const noDataText = document.createElement('p');
                    noDataText.innerText = `Nenhum detalhe encontrado para a Especialidade ${especialidade} e Ordem ${ordem}.`;
                    resultadoDiv.appendChild(noDataText);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar detalhes:', error);
            });
        }
        
        function exibirAnalisesPendentes(especialidade) {
            fetch(`/analises_pendentes/${especialidade}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-elaboracao');
                resultadoDiv.innerHTML = '';
                
                data.numeros_ar.forEach(numero_ar => {
                    const btn = document.createElement('button');
                    btn.className = 'text-button';
                    btn.innerText = `Número A.R.: ${numero_ar}`;
                    btn.onclick = function() { mostrarDetalhesElaboracao(especialidade, numero_ar); };
                    resultadoDiv.appendChild(btn);
                });
            })
            .catch(error => {
                console.error('Erro ao carregar análises pendentes:', error);
            });
        }
        
        function mostrarDetalhesElaboracao(especialidade, numero_ar) {
            fetch(`/detalhes_elaboracao/${especialidade}/${numero_ar}`)
            .then(response => response.json())
            .then(data => {
                const resultadoDiv = document.getElementById('resultado-elaboracao');
                resultadoDiv.innerHTML = '';
                
                if (data.detalhes.length > 0) {
                    data.detalhes.forEach(detalhe => {
                        // Container principal para todos os componentes
                        const containerPrincipal = document.createElement('div');
                        
                        // Adiciona o Número A.R.
                        const numeroARText = document.createElement('h3');
                        numeroARText.innerText = `Número A.R.: ${detalhe.numero_ar}`;
                        containerPrincipal.appendChild(numeroARText);
                        
                        // Adiciona a Ordem
                        const ordemText = document.createElement('h4');
                        ordemText.innerText = `Ordem: ${detalhe.ordem}`;
                        containerPrincipal.appendChild(ordemText);
                        
                        // Campo para Serviço
                        const servicoLabel = document.createElement('label');
                        servicoLabel.innerText = 'Serviço:';
                        containerPrincipal.appendChild(servicoLabel);
                        
                        const servicoInput = document.createElement('input');
                        servicoInput.type = 'text';
                        servicoInput.value = detalhe.servico || '';
                        servicoInput.id = `servico-${detalhe.id}`;
                        containerPrincipal.appendChild(servicoInput);
                        
                        // Campo para Equipamento
                        const equipamentoLabel = document.createElement('label');
                        equipamentoLabel.innerText = 'Equipamento:';
                        containerPrincipal.appendChild(equipamentoLabel);
                        
                        const equipamentoInput = document.createElement('input');
                        equipamentoInput.type = 'text';
                        equipamentoInput.value = detalhe.equipamento || '';
                        equipamentoInput.id = `equipamento-${detalhe.id}`;
                        containerPrincipal.appendChild(equipamentoInput);
                        
                        // Dropdown para Executante
                        const executanteLabel = document.createElement('label');
                        executanteLabel.innerText = 'Executante:';
                        containerPrincipal.appendChild(executanteLabel);
                        
                        const executanteSelect = document.createElement('select');
                        executanteSelect.id = `executante-${detalhe.id}`;
                        ['Executante 1', 'Executante 2'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.executante === opt) {
                                option.selected = true;
                            }
                            executanteSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(executanteSelect);
                        
                        // Dropdown para Operador
                        const operadorLabel = document.createElement('label');
                        operadorLabel.innerText = 'Operador:';
                        containerPrincipal.appendChild(operadorLabel);
                        
                        const operadorSelect = document.createElement('select');
                        operadorSelect.id = `operador-${detalhe.id}`;
                        ['Operador 1', 'Operador 2'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.operador === opt) {
                                option.selected = true;
                            }
                            operadorSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(operadorSelect);
                        
                        // Dropdown para SMS
                        const smsLabel = document.createElement('label');
                        smsLabel.innerText = 'SMS:';
                        containerPrincipal.appendChild(smsLabel);
                        
                        const smsSelect = document.createElement('select');
                        smsSelect.id = `sms-${detalhe.id}`;
                        ['SMS 1', 'SMS 2'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.sms === opt) {
                                option.selected = true;
                            }
                            smsSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(smsSelect);
                        
                        // Dropdown para Perigos
                        const perigoLabel = document.createElement('label');
                        perigoLabel.innerText = 'Perigos:';
                        containerPrincipal.appendChild(perigoLabel);
                        
                        const perigoSelect = document.createElement('select');
                        perigoSelect.id = `perigo-${detalhe.id}`;
                        ['Queda', 'Choque Elétrico', 'Incêndio'].forEach(opt => {
                            const option = document.createElement('option');
                            option.value = opt;
                            option.text = opt;
                            if (detalhe.perigo === opt) {
                                option.selected = true;
                            }
                            perigoSelect.appendChild(option);
                        });
                        containerPrincipal.appendChild(perigoSelect);
                        
                        // Botão para mostrar/ocultar as opções
                        const btnToggleOpcoes = document.createElement('button');
                        btnToggleOpcoes.className = 'button';
                        btnToggleOpcoes.innerText = 'Mostrar Opções';
                        btnToggleOpcoes.onclick = function() {
                            const containerOpcoes = document.getElementById(`opcoes-${detalhe.id}`);
                            containerOpcoes.classList.toggle('hidden');
                            btnToggleOpcoes.innerText = containerOpcoes.classList.contains('hidden') ? 'Mostrar Opções' : 'Ocultar Opções';
                        };
                        containerPrincipal.appendChild(btnToggleOpcoes);
                        
                        // Container para as opções (checkboxes)
                        const containerOpcoes = document.createElement('div');
                        containerOpcoes.id = `opcoes-${detalhe.id}`;
                        containerOpcoes.className = 'hidden';
                        
                        // Lista de perguntas
                        const perguntas = [
                            "Falta procedimento específico ou padrão básico de segurança para execução da intervenção ou é necessário alterar o padrão de execução existente?",
                            "A intervenção é realizada em local não projetado para ocupação humana contínua ou possua meios limitados de entrada e saída ou a ventilação existente é insuficiente para remover contaminantes ou possa existir a deficiência ou enriquecimento de oxigênio?",
                            "Na intervenção pode haver contato direto com produtos inflamáveis ou tóxicos?",
                            "A intervenção será realizada em instalação elétrica energizada com tensão igual ou superior a 50Vca ou 120 Vcc de forma não prevista em padrão de execução específico?",
                            "Na intervenção pode haver contato com partes desprotegidas de equipamento ou com alta temperatura ou pressurizado?",
                            "No local da intervenção existe mais de uma disciplina de manutenção ou engenharia atuando simultaneamente que acarretem riscos às equipes ou a equipamentos/sistemas vizinhos?",
                            "A elevação de carga é considerada movimentação crítica conforme padrão PE-1PBR-1428?",
                            "A intervenção envolve escavações, perfurações, fundações, de forma não prevista no padrão PE-1PBR-01426 - Segurança em Serviços de Escavação e Intervenção no Solo?",
                            "A intervenção é realizada em local acima de 2m do piso de referência (nível, superfície ou plataforma considerada como nível zero para caracterização do trabalho em altura) de forma não prevista em padrão de execução específico e na NR-35 e expõe o trabalhador a risco de queda?"
                        ];
                        
                        // Adiciona as opções ao container de opções
                        perguntas.forEach((pergunta, idx) => {
                            const checkboxRow = document.createElement('div');
                            
                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.id = `opcao-${detalhe.id}-${idx + 1}`;
                            checkbox.checked = detalhe[`opcao_${idx + 1}`] || false;
                            
                            const perguntaLabel = document.createElement('label');
                            perguntaLabel.htmlFor = `opcao-${detalhe.id}-${idx + 1}`;
                            perguntaLabel.innerText = pergunta;
                            
                            checkboxRow.appendChild(checkbox);
                            checkboxRow.appendChild(perguntaLabel);
                            containerOpcoes.appendChild(checkboxRow);
                        });
                        
                        containerPrincipal.appendChild(containerOpcoes);
                        
                        // Botão para salvar as alterações
                        const btnSalvar = document.createElement('button');
                        btnSalvar.className = 'button';
                        btnSalvar.innerText = 'Salvar';
                        btnSalvar.onclick = function() {
                            // Coletando os valores
                            const servicoValue = document.getElementById(`servico-${detalhe.id}`).value;
                            const equipamentoValue = document.getElementById(`equipamento-${detalhe.id}`).value;
                            const executanteValue = document.getElementById(`executante-${detalhe.id}`).value;
                            const operadorValue = document.getElementById(`operador-${detalhe.id}`).value;
                            const smsValue = document.getElementById(`sms-${detalhe.id}`).value;
                            const perigoValue = document.getElementById(`perigo-${detalhe.id}`).value;
                            
                            // Coletando os estados dos checkboxes
                            const checkboxesValues = {};
                            perguntas.forEach((_, idx) => {
                                const checkboxId = `opcao-${detalhe.id}-${idx + 1}`;
                                checkboxesValues[`opcao_${idx + 1}`] = document.getElementById(checkboxId).checked;
                            });
                            
                            // Enviando os dados para o servidor
                            fetch('/salvar_alteracoes', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    id: detalhe.id,
                                    servico: servicoValue,
                                    equipamento: equipamentoValue,
                                    executante: executanteValue,
                                    operador: operadorValue,
                                    sms: smsValue,
                                    perigo: perigoValue,
                                    checkboxes: checkboxesValues
                                })
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    alert('Alterações salvas com sucesso!');
                                } else {
                                    alert('Erro ao salvar alterações: ' + data.message);
                                }
                            })
                            .catch(error => {
                                console.error('Erro:', error);
                                alert('Erro ao salvar alterações.');
                            });
                        };
                        containerPrincipal.appendChild(btnSalvar);
                        
                        resultadoDiv.appendChild(containerPrincipal);
                        resultadoDiv.appendChild(document.createElement('hr'));
                    });
                } else {
                    const noDataText = document.createElement('p');
                    noDataText.innerText = `Nenhum detalhe encontrado para a Especialidade ${especialidade} e Número A.R. ${numero_ar}.`;
                    resultadoDiv.appendChild(noDataText);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar detalhes de elaboração:', error);
            });
        }
        
        // Inicialização quando o arquivo é carregado
        document.getElementById('planilha').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('planilha', file);
                
                                fetch('/carregar_planilha', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = data.message;
                    if (data.success) {
                        carregarEspecialidades();
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('status').innerText = 'Erro ao carregar o arquivo.';
                });
            }
        });
        
        // Executa ao carregar a página
        atualizarUnidade();
        
        // Carregar credenciais salvas, se existirem
        fetch('/carregar_credenciais')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.usuario) document.getElementById('usuario').value = data.usuario;
                if (data.empresa) document.getElementById('empresa').value = data.empresa;
                if (data.area) {
                    document.getElementById('area').value = data.area;
                    atualizarUnidade();
                }
                if (data.unidade) {
                    if (data.area === 'GAS NATURAL&ENERGIA') {
                        document.getElementById('unidadeGas').value = data.unidade;
                    } else {
                        document.getElementById('unidadeRef').value = data.unidade;
                    }
                }
            }
        })
        .catch(error => {
            console.error('Erro ao carregar credenciais:', error);
        });
    </script>
</body>
</html>
"""

# Criar arquivo HTML
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Rotas da aplicação Flask
"""@app.route('/')
def index():
    return render_template('index.html')"""

"""@app.route('/processar_form', methods=['POST'])
def processar_form():
    global usuario, senha, data, caminho_arquivo
    
    if 'planilha' in request.files:
        arquivo = request.files['planilha']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            os.makedirs('uploads', exist_ok=True)
            arquivo.save(caminho_arquivo)
    
    usuario = request.form.get('usuario', '')
    senha = request.form.get('senha', '')
    data = request.form.get('data', '')
    
    action = request.form.get('action', '')
    
    try:
        if action == 'elaborar_pts':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidadeGas', '')
            else:
                unidade_selecionada = request.form.get('unidadeRef', '')
            
            if not usuario or not senha or not data or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            elaborar_pts(usuario, senha, data, caminho_arquivo, empresa_selecionada, area_selecionada, unidade_selecionada)
            return jsonify({
                'success': True,
                'message': f'PTs elaboradas com sucesso para {os.path.basename(caminho_arquivo)}!'
            })
            
        elif action == 'consultar_ar':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidadeGas', '')
            else:
                unidade_selecionada = request.form.get('unidadeRef', '')
            
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            consultar_ar(usuario, senha, caminho_arquivo, empresa_selecionada, area_selecionada, unidade_selecionada)
            return jsonify({
                'success': True,
                'message': f'Consultando ARs para {usuario}...'
            })
            
        elif action == 'elaborar_ar':
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            elaborar_ar(usuario, senha, caminho_arquivo)
            return jsonify({
                'success': True,
                'message': f'Elaborando ARs para {usuario}...'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro: {str(e)}'
        })
    
    return jsonify({
        'success': True,
        'message': 'Formulário processado com sucesso!'
    })"""
@app.route('/css')
def css():
    return app.send_static_file('style.css')

@app.route('/carregar_planilha', methods=['POST'])
def carregar_planilha():
    global df, especialidades, caminho_arquivo
    
    if 'planilha' in request.files:
        arquivo = request.files['planilha']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            os.makedirs('uploads', exist_ok=True)
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            arquivo.save(caminho_arquivo)
            
            try:
                # Lê o arquivo Excel
                df = pd.read_excel(caminho_arquivo)
                
                if "ESPECIALIDADES" in df.columns:
                    especialidades = sorted(df["ESPECIALIDADES"].dropna().astype(str).unique())
                    return jsonify({
                        'success': True,
                        'message': 'Arquivo carregado com sucesso!'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': "A coluna 'ESPECIALIDADES' não foi encontrada."
                    })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro ao carregar o arquivo: {str(e)}'
                })
    
    return jsonify({
        'success': False,
        'message': 'Nenhum arquivo foi selecionado.'
    })

@app.route('/especialidades')
def get_especialidades():
    if especialidades:
        return jsonify({
            'success': True,
            'especialidades': especialidades
        })
    else:
        return jsonify({
            'success': False,
            'especialidades': [],
            'message': 'Nenhuma especialidade encontrada. Carregue um arquivo Excel primeiro.'
        })

@app.route('/ordens/<especialidade>')
def get_ordens(especialidade):
    if df is not None:
        dados_filtrados = df[df["ESPECIALIDADES"] == especialidade]
        ordens = sorted(dados_filtrados["Ordem"].dropna().unique())
        return jsonify({
            'success': True,
            'ordens': [str(ordem) for ordem in ordens]
        })
    else:
        return jsonify({
            'success': False,
            'ordens': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/detalhes/<especialidade>/<ordem>')
def get_detalhes(especialidade, ordem):
    if df is not None:
        dados_filtrados = df[(df["ESPECIALIDADES"] == especialidade) & (df["Ordem"].astype(str) == ordem)]
        detalhes = []
        
        for _, linha in dados_filtrados.iterrows():
            detalhe = {
                'ordem': str(linha['Ordem']),
                'descricao': str(linha.get('Descrição da PT', '')),
                'libra': str(linha.get('LIBRA', '')),
                'aro': str(linha.get('ARO', '')),
                'ar': str(linha.get('Número\nA.R.', ''))
            }
            detalhes.append(detalhe)
        
        return jsonify({
            'success': True,
            'detalhes': detalhes
        })
    else:
        return jsonify({
            'success': False,
            'detalhes': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/analises_pendentes/<especialidade>')
def get_analises_pendentes(especialidade):
    if df is not None:
        dados_filtrados = df[df["ESPECIALIDADES"] == especialidade]
        numeros_ar = sorted(dados_filtrados["Número\nA.R."].dropna().astype(str).unique())
        return jsonify({
            'success': True,
            'numeros_ar': numeros_ar
        })
    else:
        return jsonify({
            'success': False,
            'numeros_ar': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/detalhes_elaboracao/<especialidade>/<numero_ar>')
def get_detalhes_elaboracao(especialidade, numero_ar):
    if df is not None:
        dados_filtrados = df[(df["ESPECIALIDADES"] == especialidade) & (df["Número\nA.R."].astype(str) == numero_ar)]
        detalhes = []
        
        for idx, linha in dados_filtrados.iterrows():
            detalhe = {
                'id': idx,
                'numero_ar': str(linha.get('Número\nA.R.', '')),
                'ordem': str(linha.get('Ordem', '')),
                'servico': str(linha.get('Serviço', '')),
                'equipamento': str(linha.get('Equipamento', '')),
                'executante': str(linha.get('Executante', '')),
                'operador': str(linha.get('Operador', '')),
                'sms': str(linha.get('SMS', '')),
                'perigo': str(linha.get('Perigo', ''))
            }
            
            # Adicionar estados dos checkboxes
            for i in range(1, 10):  # 9 perguntas
                detalhe[f'opcao_{i}'] = bool(linha.get(f'Opção {i}', False))
            
            detalhes.append(detalhe)
        
        return jsonify({
            'success': True,
            'detalhes': detalhes
        })
    else:
        return jsonify({
            'success': False,
            'detalhes': [],
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })

@app.route('/salvar_alteracoes', methods=['POST'])
def salvar_alteracoes():
    global df
    
    if df is None:
        return jsonify({
            'success': False,
            'message': 'Dados não carregados. Carregue um arquivo Excel primeiro.'
        })
    
    data = request.json
    if not data:
        return jsonify({
            'success': False,
            'message': 'Dados não recebidos.'
        })
    
    try:
        idx = data.get('id')
        
        # Atualiza os valores no DataFrame
        df.at[idx, 'Serviço'] = data.get('servico', '')
        df.at[idx, 'Equipamento'] = data.get('equipamento', '')
        df.at[idx, 'Executante'] = data.get('executante', '')
        df.at[idx, 'Operador'] = data.get('operador', '')
        df.at[idx, 'SMS'] = data.get('sms', '')
        df.at[idx, 'Perigo'] = data.get('perigo', '')
        
        # Atualiza os checkboxes
        checkboxes = data.get('checkboxes', {})
        for key, value in checkboxes.items():
            # Converte 'opcao_1' para 'Opção 1'
            coluna = key.replace('opcao_', 'Opção ')
            df.at[idx, coluna] = value
        
        # Opcional: salvar o DataFrame atualizado no arquivo
        if caminho_arquivo:
            df.to_excel(caminho_arquivo, index=False)
        
        return jsonify({
            'success': True,
            'message': 'Alterações salvas com sucesso!'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao salvar alterações: {str(e)}'
        })

@app.route('/carregar_credenciais')
def carregar_credenciais():
    try:
        if os.path.exists('credentials.json'):
            with open('credentials.json', 'r', encoding='utf-8') as f:
                credentials = json.load(f)
            
            # Não enviar a senha por segurança
            if 'senha' in credentials:
                del credentials['senha']
                
            return jsonify({
                'success': True,
                **credentials
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Arquivo de credenciais não encontrado.'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar credenciais: {str(e)}'
        })
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            # Aqui você adicionaria a lógica para validar as credenciais
            # Por enquanto, apenas simulamos um login bem-sucedido
            session['username'] = username
            session['unidade'] = 'UTE-NPI'  # Exemplo
            return redirect(url_for('dashboard'))
        else:
            error = 'Usuário ou senha inválidos'
    return render_template('login.html', error=error, current_year=datetime.datetime.now().year)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    # Dados de exemplo para o dashboard
    stats = {
        'pts_total': 120,
        'pts_emitidas': 85,
        'pts_pendentes': 30,
        'ars_total': 95
    }
    
    activities = [
        {
            'icon': '📄',
            'title': 'PT Emitida',
            'description': 'PT #12345 foi emitida com sucesso',
            'time': 'Há 10 minutos'
        },
        {
            'icon': '⚠️',
            'title': 'AR Pendente',
            'description': 'AR para ordem #67890 precisa ser elaborada',
            'time': 'Há 30 minutos'
        },
        # Adicione mais atividades conforme necessário
    ]
    
    upcoming_pts = [
        {
            'ordem': '12345',
            'descricao': 'Manutenção Preventiva UG-01',
            'data': '12/11/2023',
            'status': 'Emitida'
        },
        {
            'ordem': '67890',
            'descricao': 'Inspeção de Válvulas',
            'data': '13/11/2023',
            'status': 'Pendente'
        },
        # Adicione mais PTs conforme necessário
    ]
    
    return render_template(
        'dashboard.html', 
        active_page='dashboard',
        stats=stats,
        activities=activities,
        upcoming_pts=upcoming_pts,
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[]  # Dashboard não precisa de breadcrumb
    )

@app.route('/elaborar_pts')
def elaborar_pts_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'elaborar_pts.html', 
        active_page='elaborar_pts',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Elaborar PTs', 'url': '#'}
        ]
    )

@app.route('/consultar_ar')
def consultar_ar_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'consultar_ar.html', 
        active_page='consultar_ar',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Consultar ARs', 'url': '#'}
        ]
    )
    
@app.route('/resultado')
def resultado_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    # Dados de exemplo para os resultados
    stats = {
        'pts_emitidas': 25,
        'pts_pendentes': 5,
        'erros': 2,
        'tempo_total': '15:30 min'
    }
    
    resultados = [
        {
            'ordem': '12345',
            'descricao': 'Manutenção Preventiva UG-01',
            'numero_pt': 'PT-2023-12345',
            'numero_ar': 'AR-2023-5678',
            'data': '12/11/2023',
            'status': 'Emitida'
        },
        {
            'ordem': '67890',
            'descricao': 'Inspeção de Válvulas',
            'numero_pt': None,
            'numero_ar': 'AR-2023-9012',
            'data': '13/11/2023',
            'status': 'Pendente'
        },
        {
            'ordem': '54321',
            'descricao': 'Troca de Filtros',
            'numero_pt': None,
            'numero_ar': None,
            'data': '14/11/2023',
            'status': 'Erro'
        },
        # Adicione mais resultados conforme necessário
    ]
    
    return render_template(
        'resultado.html', 
        active_page='elaborar_pts',  # Mantém ativo o menu de elaborar PTs
        stats=stats,
        resultados=resultados,
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Elaborar PTs', 'url': url_for('elaborar_pts_page')},
            {'label': 'Resultados', 'url': '#'}
        ]
    )

@app.route('/relatorios')
def relatorios_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'relatorios.html', 
        active_page='relatorios',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Relatórios', 'url': '#'}
        ]
    )

@app.route('/historico')
def historico_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'historico.html', 
        active_page='historico',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Histórico', 'url': '#'}
        ]
    )

@app.route('/configuracoes')
def configuracoes_page():
    if not session.get('username'):
        return redirect(url_for('login'))
    
    return render_template(
        'configuracoes.html', 
        active_page='configuracoes',
        today_date=datetime.datetime.now().strftime('%d/%m/%Y'),
        current_year=datetime.datetime.now().year,
        breadcrumb=[
            {'label': 'Configurações', 'url': '#'}
        ]
    )

# Rotas para API e processamento de formulários

@app.route('/processar_form', methods=['POST'])
def processar_form():
    global usuario, senha, data, caminho_arquivo
    
    # Processar arquivo se enviado
    if 'planilha' in request.files:
        arquivo = request.files['planilha']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            os.makedirs('uploads', exist_ok=True)
            arquivo.save(caminho_arquivo)
    elif 'arquivo' in request.files:  # Suporte para outro nome de campo de arquivo
        arquivo = request.files['arquivo']
        if arquivo.filename != '':
            # Salvar o arquivo temporariamente
            caminho_arquivo = os.path.join('uploads', arquivo.filename)
            os.makedirs('uploads', exist_ok=True)
            arquivo.save(caminho_arquivo)
    
    # Obter parâmetros do formulário
    usuario = request.form.get('usuario', '')
    senha = request.form.get('senha', '')
    data = request.form.get('data', '')
    action = request.form.get('action', '')
    
    try:
        if action == 'elaborar_pts':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidade', '')
            else:
                unidade_selecionada = request.form.get('unidade', '')
            
            if not usuario or not senha or not data or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # IMPORTANTE: Aqui chamamos a função elaborar_pts diretamente
            # Isso garante que ela seja chamada independentemente do tipo de resposta
            try:
                # Inicie a função em uma thread separada para não bloquear a resposta
                import threading
                
                def run_elaboration():
                    try:
                        elaborar_pts(usuario, senha, data, caminho_arquivo, 
                                    empresa_selecionada, area_selecionada, unidade_selecionada)
                        print("Elaboração de PTs concluída com sucesso!")
                    except Exception as e:
                        print(f"Erro durante a elaboração de PTs: {str(e)}")
                
                # Inicia a thread para executar a elaboração em segundo plano
                thread = threading.Thread(target=run_elaboration)
                thread.daemon = True
                thread.start()
                
                # Agora podemos responder imediatamente enquanto a elaboração continua em segundo plano
                return jsonify({
                    'success': True,
                    'message': f'Elaborando PTs para {os.path.basename(caminho_arquivo)}...',
                    'redirect': '/resultado'
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro ao iniciar elaboração: {str(e)}'
                })
        
        elif action == 'consultar_ar':
            empresa_selecionada = request.form.get('empresa', '')
            area_selecionada = request.form.get('area', '')
            
            if area_selecionada == "GAS NATURAL&ENERGIA":
                unidade_selecionada = request.form.get('unidadeGas', '')
            else:
                unidade_selecionada = request.form.get('unidadeRef', '')
            
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            try:
                consultar_ar(usuario, senha, caminho_arquivo, empresa_selecionada, 
                            area_selecionada, unidade_selecionada)
                return jsonify({
                    'success': True,
                    'message': f'Consultando ARs para {usuario}...'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro na consulta de AR: {str(e)}'
                })
        
        elif action == 'elaborar_ar':
            if not usuario or not senha or not caminho_arquivo:
                return jsonify({
                    'success': False,
                    'message': 'Por favor, preencha todos os campos e selecione um arquivo.'
                })
            
            # Chama a função do módulo elaborador
            try:
                elaborar_ar(usuario, senha, caminho_arquivo)
                return jsonify({
                    'success': True,
                    'message': f'Elaborando ARs para {usuario}...'
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Erro na elaboração de AR: {str(e)}'
                })
        
        else:
            return jsonify({
                'success': False,
                'message': 'Ação desconhecida'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro geral: {str(e)}'
        })

@app.route('/detalhes_pt/<ordem>')
def detalhes_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
        # Simulação de dados da PT
    pt_data = {
        'ordem': ordem,
        'numero_pt': f'PT-2023-{ordem}',
        'numero_ar': f'AR-2023-{int(ordem) % 10000}',
        'data': '12/11/2023',
        'status': 'Emitida',
        'descricao': 'Manutenção preventiva nos equipamentos da unidade geradora.',
        'recomendacoes': 'Utilizar EPI adequado. Verificar isolamento da área. Comunicar operação antes do início das atividades.'
    }
    
    return jsonify(pt_data)

@app.route('/imprimir_pt/<ordem>')
def imprimir_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Aqui você implementaria a geração do PDF para impressão
    # Por enquanto, apenas retorna uma mensagem
    response = make_response("Simulação de PDF da PT")
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=PT-{ordem}.pdf"
    return response

@app.route('/reprocessar_pt/<ordem>', methods=['POST'])
def reprocessar_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Simulação de reprocessamento
    time.sleep(2)  # Simula processamento
    
    # Retorna sucesso
    return jsonify({
        'success': True,
        'message': f'PT para ordem {ordem} reprocessada com sucesso!'
    })

@app.route('/erro_pt/<ordem>')
def erro_pt(ordem):
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Simulação de dados do erro
    erro_data = {
        'message': 'Não foi possível conectar ao sistema SPT.',
        'timestamp': '12/11/2023 14:35:22',
        'log': 'Error: Connection timeout after 30000ms\nAttempting to reconnect...\nFailed to reconnect: Server unavailable',
        'suggestions': [
            'Verifique sua conexão com a rede corporativa.',
            'Tente novamente em alguns minutos.',
            'Se o problema persistir, entre em contato com o suporte.'
        ]
    }
    
    return jsonify(erro_data)

@app.route('/exportar_excel')
def exportar_excel():
    if not session.get('username'):
        return jsonify({'error': 'Não autenticado'}), 401
    
    # Aqui você implementaria a geração do Excel
    # Por enquanto, apenas retorna uma mensagem
    response = make_response("Simulação de arquivo Excel")
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response.headers["Content-Disposition"] = "attachment; filename=resultados_pts.xlsx"
    return response

# Rota raiz - redireciona para login ou dashboard
@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# Função para iniciar o navegador automaticamente
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Definir função principal
def main():
    # Iniciar o navegador automaticamente quando o servidor iniciar
    threading.Timer(1.5, open_browser).start()
    
    # Iniciar o servidor Flask
    app.run(debug=True)

if __name__ == "__main__":
>>>>>>> 8a02ef36b1269fd6d4ad3388097ee8ba96cc24a8
    app.run(debug=True)