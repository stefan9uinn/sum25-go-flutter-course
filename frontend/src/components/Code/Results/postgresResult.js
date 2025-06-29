import React from 'react';
import { Typography, Divider } from 'antd';


class PostgresResult extends React.Component {

    render() {
        const { response } = this.props;

        if (!response || (typeof response !== 'object' && !Array.isArray(response))) {
            return (
                <div>
                    <Typography.Text className='code-initial-text'>Request result will appear here</Typography.Text>
                </div>
            );
        }

        return (
            <div>
                {(!response.results || (Array.isArray(response.results) ? response.results.length === 0 : Object.keys(response.results).length === 0)) ?
                    <Typography.Text className='code-initial-text'>Request result will appear here</Typography.Text> :
                    <div className="code-output-item">
                        {Array.isArray(response.results) && response.results.length >= 1 ? (
                            <div>
                                <Typography.Text className='code-text' style={{ color: '#51CB63', fontSize: '14px' }}>
                                    Success!
                                </Typography.Text>
                            </div>
                        ) : (
                            <div>
                                <Typography.Text className='code-text' style={{ color: '#c01619', fontSize: '14px' }}>
                                    Error!
                                </Typography.Text>
                            </div>
                        )}
                    </div>
                }
            </div>
        );
    }
}

export default PostgresResult;