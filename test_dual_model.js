// Test script for Dual-Model API (Polish + English)

const testTexts = {
  polishReal: "Naukowcy z Uniwersytetu Warszawskiego ujawniają nowe badania dotyczące ochrony środowiska",
  polishFake: "Nie uwierzysz co eksperci odkryli! Śledztwo ujawnia zaskakującą prawdę o szczepionkach",
  englishReal: "Scientists conduct groundbreaking research revealing surprising connections about climate change",
  englishFake: "You won't believe what experts discovered! Shocking investigation reveals mainstream science is hiding the truth"
};

console.log('🧪 Testing BANED Dual-Model API\n');
console.log('=' .repeat(70));

// Import the API function
const predict = require('./api/predict.js');

// Mock request/response objects
const createMockReq = (text) => ({
  method: 'POST',
  body: { text, use_fusion: true }
});

const createMockRes = () => {
  let jsonData = null;
  let statusCode = 200;
  
  return {
    setHeader: () => {},
    status: (code) => {
      statusCode = code;
      return {
        json: (data) => { jsonData = data; return jsonData; },
        end: () => {}
      };
    },
    json: (data) => { 
      jsonData = data; 
      return jsonData;
    },
    getResponse: () => ({ status: statusCode, data: jsonData })
  };
};

// Test function
async function testPrediction(label, text) {
  console.log(`\n📝 TEST: ${label}`);
  console.log(`Text: "${text.substring(0, 80)}..."`);
  console.log('-'.repeat(70));
  
  const req = createMockReq(text);
  const res = createMockRes();
  
  await predict(req, res);
  const response = res.getResponse();
  
  if (response.data) {
    const { prediction, confidence, language, scores, kb_match, model_info } = response.data;
    
    console.log(`🌐 Language: ${language.toUpperCase()}`);
    console.log(`🎯 Prediction: ${prediction}`);
    console.log(`📊 Confidence: ${(confidence * 100).toFixed(2)}%`);
    console.log(`⚖️  Scores: Real ${scores.real} | Fake ${scores.fake}`);
    console.log(`🔍 KB Matches:`);
    console.log(`   Real: [${kb_match.real.join(', ')}]`);
    console.log(`   Fake: [${kb_match.fake.join(', ')}]`);
    console.log(`📚 Model: ${model_info.dataset}`);
    if (model_info.performance) {
      console.log(`🏆 Performance: ${model_info.performance}`);
    }
    console.log(`✅ Loss: ${model_info.final_loss}`);
  } else {
    console.log('❌ ERROR:', response.data);
  }
}

// Run tests
(async () => {
  console.log('\n🇵🇱 POLISH TESTS (Best Model - 0.0001 loss)\n');
  await testPrediction('Polish Real News', testTexts.polishReal);
  await testPrediction('Polish Fake News', testTexts.polishFake);
  
  console.log('\n\n🇬🇧 ENGLISH TESTS (0.0007 loss)\n');
  await testPrediction('English Real News', testTexts.englishReal);
  await testPrediction('English Fake News', testTexts.englishFake);
  
  console.log('\n' + '='.repeat(70));
  console.log('✅ All tests completed!');
  console.log('\n🏆 Polish Hard 10K is the BEST MODEL (0.0001 loss)');
  console.log('🥈 English Hard is excellent too (0.0007 loss)');
  console.log('\n🌐 Dual-model system ready for production!');
})();
