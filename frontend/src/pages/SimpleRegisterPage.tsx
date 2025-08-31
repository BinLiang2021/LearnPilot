import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const SimpleRegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    name: '',
    email: '',
    password: '',
    level: 'intermediate',
    interests: '',
    daily_hours: '2.0',
    language: 'Chinese',
    registration_notes: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const submitData = {
        ...formData,
        interests: formData.interests.split(',').map(item => item.trim()).filter(item => item),
        daily_hours: parseFloat(formData.daily_hours)
      }

      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData),
      })

      const data = await response.json()

      if (response.ok) {
        setSuccess('注册成功！请等待管理员审核，审核通过后您将收到邮件通知。')
        setTimeout(() => {
          navigate('/login')
        }, 3000)
      } else {
        setError(data.detail || '注册失败')
      }
    } catch (err) {
      setError('网络错误，请重试')
      console.error('Register error:', err)
    } finally {
      setLoading(false)
    }
  }

  const formFieldStyle = {
    width: '100%',
    padding: '10px',
    border: '2px solid #e5e7eb',
    borderRadius: '6px',
    fontSize: '14px',
    outline: 'none',
    transition: 'border-color 0.2s'
  }

  const labelStyle = {
    display: 'block',
    marginBottom: '6px',
    fontWeight: '500',
    color: '#374151',
    fontSize: '14px'
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif',
      padding: '20px'
    }}>
      <div style={{
        background: 'white',
        padding: '40px',
        borderRadius: '12px',
        boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
        width: '100%',
        maxWidth: '500px'
      }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <div style={{
            width: '60px',
            height: '60px',
            backgroundColor: '#3b82f6',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto',
            marginBottom: '15px'
          }}>
            <span style={{ color: 'white', fontWeight: 'bold', fontSize: '24px' }}>LP</span>
          </div>
          <h1 style={{ margin: 0, fontSize: '28px', fontWeight: 'bold', color: '#1f2937' }}>
            注册 LearnPilot
          </h1>
          <p style={{ margin: '8px 0', color: '#6b7280', fontSize: '14px' }}>
            加入AI驱动的学术研究社区
          </p>
        </div>

        {/* Registration Form */}
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
            <div>
              <label style={labelStyle}>用户名 *</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                style={formFieldStyle}
                placeholder="用户名"
              />
            </div>
            <div>
              <label style={labelStyle}>姓名 *</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                style={formFieldStyle}
                placeholder="您的姓名"
              />
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={labelStyle}>邮箱 *</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              style={formFieldStyle}
              placeholder="your@email.com"
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={labelStyle}>密码 *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              style={formFieldStyle}
              placeholder="至少6个字符"
              minLength={6}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
            <div>
              <label style={labelStyle}>学术水平</label>
              <select
                name="level"
                value={formData.level}
                onChange={handleChange}
                style={formFieldStyle}
              >
                <option value="beginner">初学者</option>
                <option value="intermediate">中级</option>
                <option value="advanced">高级</option>
              </select>
            </div>
            <div>
              <label style={labelStyle}>每日学习时间</label>
              <select
                name="daily_hours"
                value={formData.daily_hours}
                onChange={handleChange}
                style={formFieldStyle}
              >
                <option value="0.5">0.5小时</option>
                <option value="1.0">1小时</option>
                <option value="2.0">2小时</option>
                <option value="3.0">3小时</option>
                <option value="4.0">4小时及以上</option>
              </select>
            </div>
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={labelStyle}>研究兴趣</label>
            <input
              type="text"
              name="interests"
              value={formData.interests}
              onChange={handleChange}
              style={formFieldStyle}
              placeholder="机器学习, 深度学习, 自然语言处理（用逗号分隔）"
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={labelStyle}>注册说明（可选）</label>
            <textarea
              name="registration_notes"
              value={formData.registration_notes}
              onChange={handleChange}
              style={{...formFieldStyle, height: '80px', resize: 'vertical'}}
              placeholder="简单介绍一下您的背景和使用LearnPilot的目的"
            />
          </div>

          {error && (
            <div style={{
              backgroundColor: '#fee2e2',
              color: '#dc2626',
              padding: '12px',
              borderRadius: '6px',
              marginBottom: '15px',
              fontSize: '14px'
            }}>
              {error}
            </div>
          )}

          {success && (
            <div style={{
              backgroundColor: '#d1fae5',
              color: '#065f46',
              padding: '12px',
              borderRadius: '6px',
              marginBottom: '15px',
              fontSize: '14px'
            }}>
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '12px',
              backgroundColor: loading ? '#9ca3af' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.2s'
            }}
          >
            {loading ? '注册中...' : '注册账户'}
          </button>
        </form>

        <div style={{ 
          textAlign: 'center', 
          marginTop: '25px',
          paddingTop: '20px',
          borderTop: '1px solid #e5e7eb'
        }}>
          <span style={{ color: '#6b7280', fontSize: '14px' }}>
            已有账户？{' '}
            <Link 
              to="/login" 
              style={{ 
                color: '#3b82f6', 
                textDecoration: 'none',
                fontWeight: '500'
              }}
            >
              立即登录
            </Link>
          </span>
        </div>
      </div>
    </div>
  )
}

export default SimpleRegisterPage