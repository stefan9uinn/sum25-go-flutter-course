import React from "react";
import { getClassromsById } from '../../api';
import { Typography } from "antd";
import './Classrooms.css';

const { Title, Paragraph, Text, Link } = Typography;

class ClassRooms extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      studentId: 1,
      classrooms: []
    }
  }

  async componentDidMount() {
    try {
      const classrooms = await getClassromsById(this.state.studentId);
      this.setState({ classrooms });
    } catch (error) {
      console.error("Failed to fetch classrooms:", error);
    }
  }

  render() {
    return (
      <div className="classrooms">
        <Title style={{
          color: "#fff",
          fontSize: 45,
          fontFamily: "'Noto Sans', sans-serif",
          fontWeight: 600,
          marginBottom: 10
        }}>Will be <Text style={{
          color: "#51CB63",
          fontSize: 45,
          fontFamily: "'Noto Sans', sans-serif",
          fontWeight: 600,
          marginBottom: 10
        }}>later</Text>!</Title>

        <ul>
          {this.state.classrooms.map(classroom => (
            <li key={classroom.id}>
              <Text strong>{classroom.title}</Text>: {classroom.description}
            </li>
          ))}
        </ul>
      </div>
    );
  }


}

export default ClassRooms;