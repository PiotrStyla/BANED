// TensorFlow.js Model for Fake News Detection
// This creates a simple neural network for text classification

class FakeNewsMLModel {
  constructor() {
    this.model = null;
    this.vocabulary = new Map();
    this.maxSequenceLength = 100;
    this.vocabSize = 1000;
    this.isLoaded = false;
  }

  // Create a simple neural network model
  createModel() {
    const tf = require('@tensorflow/tfjs-node');
    
    const model = tf.sequential({
      layers: [
        // Embedding layer
        tf.layers.embedding({
          inputDim: this.vocabSize,
          outputDim: 64,
          inputLength: this.maxSequenceLength,
          name: 'embedding'
        }),
        
        // Global average pooling to reduce dimensions
        tf.layers.globalAveragePooling1d({ name: 'global_avg_pool' }),
        
        // Dense layers with dropout for regularization
        tf.layers.dense({
          units: 64,
          activation: 'relu',
          name: 'dense1'
        }),
        tf.layers.dropout({ rate: 0.5, name: 'dropout1' }),
        
        tf.layers.dense({
          units: 32,
          activation: 'relu',
          name: 'dense2'
        }),
        tf.layers.dropout({ rate: 0.3, name: 'dropout2' }),
        
        // Output layer for binary classification
        tf.layers.dense({
          units: 1,
          activation: 'sigmoid',
          name: 'output'
        })
      ]
    });

    // Compile the model
    model.compile({
      optimizer: tf.train.adam(0.001),
      loss: 'binaryCrossentropy',
      metrics: ['accuracy']
    });

    return model;
  }

  // Build vocabulary from training data
  buildVocabulary(texts) {
    const wordCounts = new Map();
    
    // Count word frequencies
    texts.forEach(text => {
      const words = this.tokenize(text);
      words.forEach(word => {
        wordCounts.set(word, (wordCounts.get(word) || 0) + 1);
      });
    });

    // Sort by frequency and take top words
    const sortedWords = Array.from(wordCounts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, this.vocabSize - 2); // Reserve 2 slots for special tokens

    // Build vocabulary map
    this.vocabulary.set('<PAD>', 0);
    this.vocabulary.set('<UNK>', 1);
    
    sortedWords.forEach(([word], index) => {
      this.vocabulary.set(word, index + 2);
    });
  }

  // Simple tokenization
  tokenize(text) {
    return text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 0);
  }

  // Convert text to sequence of integers
  textToSequence(text) {
    const words = this.tokenize(text);
    const sequence = words.map(word => 
      this.vocabulary.get(word) || this.vocabulary.get('<UNK>')
    );

    // Pad or truncate to fixed length
    if (sequence.length > this.maxSequenceLength) {
      return sequence.slice(0, this.maxSequenceLength);
    } else {
      const padding = new Array(this.maxSequenceLength - sequence.length).fill(0);
      return sequence.concat(padding);
    }
  }

  // Generate synthetic training data
  generateTrainingData() {
    const fakeNews = [
      "SHOCKING miracle cure doctors don't want you to know about this secret",
      "You won't believe what this one weird trick can do for your health",
      "BREAKING conspiracy exposed government cover-up revealed by insider",
      "Amazing discovery that will change everything doctors hate this",
      "Incredible secret big pharma doesn't want revealed to the public",
      "Stunning revelation about hidden truth they tried to suppress",
      "Explosive evidence of massive cover-up finally leaked to media",
      "Unbelievable cure that pharmaceutical companies tried to ban",
      "Mind-blowing secret that will shock you to your core today",
      "Devastating truth about what they've been hiding from us"
    ];

    const realNews = [
      "Department of Health announces new vaccination program according to official sources",
      "University researchers published peer-reviewed study in medical journal",
      "Government spokesperson confirmed policy implementation based on expert analysis",
      "Scientific evidence shows effectiveness of treatment in clinical trials",
      "Ministry officials reported findings from comprehensive investigation",
      "Research institute published data analysis in academic publication",
      "Health authorities confirmed safety measures following expert review",
      "Official statement released by government agency regarding new policy",
      "Medical professionals recommend treatment based on clinical evidence",
      "Academic researchers present findings at international conference"
    ];

    const texts = [...fakeNews, ...realNews];
    const labels = [
      ...new Array(fakeNews.length).fill(0), // 0 for fake
      ...new Array(realNews.length).fill(1)  // 1 for real
    ];

    return { texts, labels };
  }

  // Train the model
  async trainModel() {
    const tf = require('@tensorflow/tfjs-node');
    
    try {
      // Generate training data
      const { texts, labels } = this.generateTrainingData();
      
      // Build vocabulary
      this.buildVocabulary(texts);
      
      // Convert texts to sequences
      const sequences = texts.map(text => this.textToSequence(text));
      
      // Create tensors
      const xs = tf.tensor2d(sequences);
      const ys = tf.tensor2d(labels, [labels.length, 1]);
      
      // Create model
      this.model = this.createModel();
      
      console.log('Training TensorFlow.js model...');
      
      // Train the model
      const history = await this.model.fit(xs, ys, {
        epochs: 50,
        batchSize: 4,
        validationSplit: 0.2,
        verbose: 0,
        callbacks: {
          onEpochEnd: (epoch, logs) => {
            if (epoch % 10 === 0) {
              console.log(`Epoch ${epoch}: loss = ${logs.loss.toFixed(4)}, accuracy = ${logs.acc.toFixed(4)}`);
            }
          }
        }
      });
      
      // Clean up tensors
      xs.dispose();
      ys.dispose();
      
      this.isLoaded = true;
      console.log('TensorFlow.js model training completed!');
      
      return {
        success: true,
        finalLoss: history.history.loss[history.history.loss.length - 1],
        finalAccuracy: history.history.acc[history.history.acc.length - 1]
      };
      
    } catch (error) {
      console.error('Error training model:', error);
      return { success: false, error: error.message };
    }
  }

  // Make prediction
  async predict(text) {
    if (!this.model || !this.isLoaded) {
      throw new Error('Model not loaded. Please train the model first.');
    }

    const tf = require('@tensorflow/tfjs-node');
    
    try {
      // Convert text to sequence
      const sequence = this.textToSequence(text);
      
      // Create tensor
      const input = tf.tensor2d([sequence]);
      
      // Make prediction
      const prediction = this.model.predict(input);
      const probability = await prediction.data();
      
      // Clean up tensors
      input.dispose();
      prediction.dispose();
      
      const realProbability = probability[0];
      const fakeProbability = 1 - realProbability;
      
      return {
        prediction: realProbability > 0.5 ? 'REAL' : 'FAKE',
        confidence: Math.max(realProbability, fakeProbability),
        real_probability: realProbability,
        fake_probability: fakeProbability,
        method: 'tensorflow_neural_network'
      };
      
    } catch (error) {
      console.error('Error making prediction:', error);
      throw error;
    }
  }

  // Get model info
  getModelInfo() {
    return {
      isLoaded: this.isLoaded,
      vocabSize: this.vocabSize,
      maxSequenceLength: this.maxSequenceLength,
      vocabularyBuilt: this.vocabulary.size > 0,
      modelArchitecture: this.model ? 'Sequential Neural Network' : 'Not created'
    };
  }
}

module.exports = FakeNewsMLModel;
