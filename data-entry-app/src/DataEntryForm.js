import React, { useState } from 'react';

function DataEntryForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // 处理表单提交逻辑
    console.log('表单数据:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>姓名:</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>邮箱:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">提交</button>
    </form>
  );
}

export default DataEntryForm;