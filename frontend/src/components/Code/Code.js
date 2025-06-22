import React from 'react';
import { getCode } from '../../api';
import { getIState } from '../../api';
import CodeInput from './codeInput';
import OutputInputs from './output';
import { Button, FloatButton, Typography } from 'antd';
import { FaRegLightbulb } from "react-icons/fa";
import HintModal from './hintModal';
import './Code.css';

class Code extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      response: {
      },
      db_state: {},
      isModalOpen: false,
      isLoading: false,
    }

    this.getIt = this.getIt.bind(this);
    this.getInitialState = this.getInitialState.bind(this);
    this.open = this.open.bind(this);
    this.close = this.close.bind(this);
    this.setLoading = this.setLoading.bind(this);
  }
  render() {
    return (
      <div className="code-container">
        <Button className='my-back-button' style={{ height: '35px', fontSize: '15px' }} onClick={() => this.props.handleButtonClick("template")}>Back</Button>
        <main>
          <CodeInput getIt={(text, chosenDb) => this.getIt(text, chosenDb)} isLoading={this.state.isLoading} />
        </main>
        <aside className="code-aside">
          <OutputInputs response={this.state.response} db_state={this.state.db_state} />
        </aside>
        <FloatButton icon={<FaRegLightbulb />} type="basic" className='lamp' onClick={this.open} tooltip="Command Tips" />
        <HintModal title={<Typography.Text className='modal-title'>Types of command for <Typography.Text className='modal-title' style={{ color: '#51CB63' }}>ChromaDB</Typography.Text> </Typography.Text>} onCancel={this.close} open={this.state.isModalOpen} />
      </div>
    );
  }

  setLoading = (loading) => {
    this.setState({ isLoading: loading });
  }

  open = () => {
    this.setState({ isModalOpen: true });
    console.log(this.state.isModalOpen);
  };

  close = () => {
    this.setState({ isModalOpen: false });
  }

  componentDidMount() {
    if (this.props.isLogin === true && Object.keys(this.state.db_state).length === 0) {
      this.getInitialState();
    }
  }

  getInitialState() {
    this.setLoading(true);
    let string = (this.props.getCookie("login") + this.props.getCookie("password"));
    getIState(string.hashCode())
      .then(data => {
        this.setState({ db_state: data }, () => {
          console.log(this.state.db_state);
        });
        this.setLoading(false);
      })
      .catch(error => {
        console.error('Error:', error);
        this.setLoading(false);
      });
  }

  getIt(text, chosenDb) {
    if (this.props.isLogin === false) {
      alert("Please log in to run the code");
      return;
    }
    if (chosenDb === "Choose DB") {
      alert("Please choose a database");
      return;
    } else if (text === "" || text === null) {
      alert("Please write your code");
      return;
    }
    if (chosenDb === "PostgreSQL") {
      alert("Please choose another DB for now");
      return;
    }
    if (chosenDb === "SQLite") {
      alert("Please choose another DB for now");
      return;
    }
    if (chosenDb === "MongoDB") {
      alert("Please choose another DB for now");
      return;
    }
    if (chosenDb === "ChromaDB") {
      this.setLoading(true);
      const error = {
        message: "Please try once again, there is an error in your code",
      }
      let string = (this.props.getCookie("login") + this.props.getCookie("password"));
      if (!text.includes('\n')) {
        getCode(text, string.hashCode())
          .then(data => {
            data === "Error" ? this.setState({ response: error }) : this.setState({ response: data }, () => {
              console.log(this.state.response)
            });
            this.setLoading(false);
          })
          .catch(error => console.error('Error:', error));
      }
      else{
        let commands = text.split('\n');
        commands.forEach((item, index) => {
          this.setLoading(true);
          getCode(item, string.hashCode())
          .then(data => {
            data === "Error" ? this.setState({ response: error }) : this.setState({ response: data }, () => {
              console.log(this.state.response)
            });
            this.setLoading(false);
          })
          .catch(error => console.error('Error:', error));
        });
      }

    }
  }
}


String.prototype.hashCode = function () {
  let hash = 0;
  for (let i = 0; i < this.length; i++) {
    const chr = this.charCodeAt(i);
    hash = ((hash << 5) - hash) + chr;
    hash |= 0;
  }
  return hash;
};


export default Code;