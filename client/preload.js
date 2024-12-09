const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('api', {
  fetchMessage: async (message) => {
    try {
      const response = await fetch(`http://localhost:8000/?message=${encodeURIComponent(message)}`);
      const data = await response.json();
      return data.message;
    } catch (error) {
      console.error('Error:', error);
      return 'Error fetching message';
    }
  }
});