load("../data/weights.mat")
load("../data/sets.mat")

predTrain = predict(Theta1, Theta2, training_X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(predTrain == training_y)) * 100);

predTest = predict(Theta1, Theta2, test_X);

fprintf('\nTest Set Accuracy: %f\n', mean(double(predTest == test_y)) * 100);
