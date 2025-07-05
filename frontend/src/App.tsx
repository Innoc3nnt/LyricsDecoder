import React, { useState } from 'react';
import axios from 'axios';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';

interface GraphData {
  nodes: any[];
  edges: any[];
}

const App: React.FC = () => {
  const [query, setQuery] = useState('');
  const [graph, setGraph] = useState<GraphData | null>(null);

  const search = async () => {
    const res = await axios.get('/api/search', { params: { q: query } });
    if (res.data && res.data.hits && res.data.hits.length > 0) {
      const songId = res.data.hits[0].result.id;
      const g = await axios.get(`/api/graph/${songId}`);
      setGraph(g.data);
    }
  };

  return (
    <div style={{ height: '100%' }}>
      <div style={{ padding: 10 }}>
        <input value={query} onChange={e => setQuery(e.target.value)} />
        <button onClick={search}>Search</button>
      </div>
      {graph && (
        <CytoscapeComponent
          elements={[...graph.nodes, ...graph.edges]}
          style={{ width: '100%', height: '90%' }}
          layout={{ name: 'cose' }}
        />
      )}
    </div>
  );
};

export default App;
