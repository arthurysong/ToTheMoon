% load the data.
% divide data to train and test
% learn params using train
% test params using test set.

disp("loading and preparing data...")
data = load('-ascii', '../data/nn_data.m');

m = size(data, 1);
# 4042 inputs # 1 output label
X = data(:, 1:4042);
y = data(:, 4043);

X_norm = featureNormalize(X);

% training data is 80%
training_set_size = int32(m * .8);
test_set_size = m - training_set_size;

training_X = X_norm(1:training_set_size, :);
test_X = X_norm(training_set_size + 1:m, :);

training_y = y(1:training_set_size, :);
test_y = y(training_set_size + 1:m, :);

save("../data/sets.mat", 'training_X', 'training_y', 'test_X', 'test_y')

input_layer_size = 4042;
hidden_layer_size = 300;
num_labels = 3;

% lets do one hidden layer that is 300
% theta1 will be 4043 x 300
% theta2 will be 301 x 3

% add bias to X
disp("initalizing random theta...")
theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
theta2 = randInitializeWeights(hidden_layer_size, num_labels);
initial_nn_params = [theta1(:) ; theta2(:)];

% % display some set sizes.
% disp(size(training_X))
% disp(size(theta1))
% disp(size(theta2))
% disp(size(initial_nn_params))
% disp(size(training_y))

% % test nnCostFunction really quick
% lambda = 0;
% J = nnCostFunction(initial_nn_params, input_layer_size, hidden_layer_size, ...
%                    num_labels, training_X, training_y, lambda);

% fprintf(['Cost at parameters (loaded from ex4weights): %f '...
%          '\n(this value should be about 0.287629)\n'], J);

% fprintf('\nProgram paused. Press enter to continue.\n');
% pause;
nn_params = initial_nn_params;
total_cost = 0;

% for i = 1:size(training_X, 1)
for i = 1:10
  disp(["run gradient descent using example ", num2str(i)])
  lambda = 1;
  options = optimset('MaxIter', 1);
  row_X = training_X(i, :);
  row_X(1, 1:10)
  row_y = training_y(i, :)
  [cost] = nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, row_X, row_y, lambda)
  costFunction = @(p) nnCostFunction(p, ...
                                    input_layer_size, ...
                                    hidden_layer_size, ...
                                    num_labels, row_X, row_y, lambda);


  [nn_params, cost] = fmincg(costFunction, nn_params, options);
  cost
  total_cost = total_cost + cost;
  avg_cost = total_cost / i
endfor

% lambda = 1;
% options = optimset('MaxIter', 50);

% costFunction = @(p) nnCostFunction(p, ...
%                                    input_layer_size, ...
%                                    hidden_layer_size, ...
%                                    num_labels, training_X(1:4, :), training_y(1:4, :), lambda);

% disp("run gradient fmincg with costFunction...")
% [nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

disp("epochs finished...")

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

save("../data/weights.mat", 'Theta1', 'Theta2');

disp("weights saved!")
disp("learning finished")