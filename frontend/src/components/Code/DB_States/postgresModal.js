import React from "react"
import { Modal, Typography } from "antd";
import { TbPointFilled } from "react-icons/tb";

class PostgresModal extends React.Component {
  render() {
    return (
      <Modal
        title={this.props.title}
        open={this.props.open}
        onCancel={this.props.onCancel}
        footer={null}
        width={this.props.width || 720}
        centered
        destroyOnClose
        className="my-modal"
      >
        <div > 
           
        </div>
        
        
      </Modal>
    )
  }

  
}

export default PostgresModal