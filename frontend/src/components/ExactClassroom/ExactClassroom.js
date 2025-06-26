import React from "react";
import { Typography, Button } from "antd";
import './ExactClassroom.css';
import image from "../../img/Screen.jpg"

const { Title, Paragraph, Text, Link } = Typography;

class ExactClassroom extends React.Component {
  
  render() {
    const classroom = this.props.classroom;
    
    return (
      <div className="classroom">
        <Title style={{
          marginTop: 30,
          color: "#51CB63",
          fontSize: 45,
          fontFamily: "'Noto Sans', sans-serif",
          fontWeight: 600,
          marginBottom: 10
        }}>
          {classroom.name}
        </Title>
        <Text>Primary Instructor: {classroom.teacher}</Text><br />
        <Text>Number of Students: {classroom.numberOfStudents}</Text><br />
        <Text>Created: {classroom.date}</Text>
      </div>
    );
  }
}

export default ExactClassroom;