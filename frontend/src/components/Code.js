import React from 'react';
import { Button, Typography, Upload } from 'antd';
import { message, Select } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { getCode } from '../api'; // Assuming getCode is defined in api.js

const uploadProps = {
  name: 'file',
  action: '/upload',
  headers: { authorization: 'auth' },
  onChange(info) {
    const { status, name } = info.file;
    if (status === 'done') {
      message.success(`${name} успешно загружен`);
    } else if (status === 'error') {
      message.error(`${name} не смог загрузиться`);
    }
  },
};

class Code extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      code: "",
      chosenDb: "Choose DB",
      response: {},
    }
  }
  render() {
    return (
      <div className="code-container">
        <main>
          <p className="account-text">Write your code or <span><Upload {...uploadProps}>
            <Button icon={<UploadOutlined />} className='my-orange-button-outline' > Import File</Button>
          </Upload></span></p>
          <textarea className='code-textarea' placeholder='Will your code appear here?' onChange={(data) => this.setState({ code: data.target.value })}></textarea>
          <div className='code-buttons' style={{ display: 'flex', flexDirection: 'row', justifyContent: 'right' }}>
            <Select
              className='code-select'
              defaultValue="Choose DB"
              style={{ width: 190, marginRight: '10px', marginTop: '10px' }}
              options={[
                { value: 'Choose DB', label: 'Choose DB', disabled: true },
                { value: 'PostgreSQL', label: 'PostgreSQL' },
                { value: 'SQLite', label: 'SQLite' },
                { value: 'MongoDB', label: 'MongoDB' },
                { value: 'Vector-Based Database', label: 'Vector-Based Database' },
              ]}
              onChange={value => this.setState({ chosenDb: value })}
            />
            < Button className='my-orange-button-outline' type="primary" style={{ marginTop: '10px', marginLeft: '0px' }} onClick={() => this.getIt(this.state.code)}>Run Code</Button>
          </div>
        </main>
        <aside className="code-aside">
          <p className="account-text">Current DB state:</p>
          <div className="code-output">
            <Typography.Text className='code-text'>Document Id:</Typography.Text>
          </div>
          <p className="account-text" style={{ marginTop: '10px' }} >Request Result:</p>
          <div className="code-result">
            <Typography.Text className='code-text'></Typography.Text>
          </div>
        </aside>
      </div>
    );
  }
  getIt(text) {
    if (this.state.chosenDb === "Choose DB") {
      alert("Please choose a database");
      return;
    } else if (text === "" || text === null) {
      alert("Please write your code");
      return;
    }
    if (this.state.chosenDb === "PostgreSQL") {

    }
    if (this.state.chosenDb === "SQLite") {

    }
    if (this.state.chosenDb === "MongoDB") {

    }
    if (this.state.chosenDb === "Vector-Based Database") {
      getCode(text)
        .then(data => this.setState({ response: data }, () => {
          console.log(this.state.response)
        }))
        .catch(error => console.error('Error:', error));
    }
  }
}

export default Code;