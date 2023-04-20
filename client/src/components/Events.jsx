import React from 'react';

export function Events({ RecievedData }) {
  return (
    <ul>
    {
      RecievedData.map((index, item) =>
        <li key={ index }>{ item.value }</li>
      )
    }
    </ul>
  );
}