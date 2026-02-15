import React from 'react'
import './Modal.css'

function Modal({ 
  isVisible, 
  onClose, 
  title = 'Atención', 
  message, 
  icon = 'fa-exclamation-circle',
  iconColor = '#e74c3c',
  showCancel = false,
  onConfirm = null,
  confirmText = 'Entendido'
}) {
  if (!isVisible) return null

  return (
    <div className="modal-overlay show">
      <div className="modal-content">
        <span className="modal-icon" style={{ color: iconColor }}>
          <i className={`fas ${icon}`}></i>
        </span>
        <h3>{title}</h3>
        <p>{message}</p>
        <div className="modal-actions">
          {showCancel && (
            <button 
              type="button" 
              className="btn-modal btn-cancel" 
              onClick={onClose}
            >
              Cancelar
            </button>
          )}
          <button 
            type="button" 
            className="btn-modal" 
            onClick={onConfirm || onClose}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Modal
