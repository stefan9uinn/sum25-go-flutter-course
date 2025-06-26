import React from "react";
import { Typography, Button } from "antd";
import './ExactClassroom.css';
import image from "../../img/Screen.jpg"

const { Title, Paragraph, Text, Link } = Typography;

class ExactClassroom extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      id: 24,
      name: "Introduction to Programmming",
      teacher: "Zlata Schedrikova",
      numberOfStudents: 324,
      date: 23
    }
  }


  render() {
    return (
      <div className="classroom">
        <Title style={{
          marginTop: 30,
          color: "#51CB63",
          fontSize: 45,
          fontFamily: "'Noto Sans', sans-serif",
          fontWeight: 600,
          marginBottom: 10
        }}>Will be <Text style={{
          color: "#fff",
          fontSize: 45,
          fontFamily: "'Noto Sans', sans-serif",
          fontWeight: 600,
          marginBottom: 10
        }}>later</Text>
        </Title>
        
          
      </div>
    );
  }
}

export default ExactClassroom;