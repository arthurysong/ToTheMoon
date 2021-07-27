function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)

Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

m = size(X, 1);
         
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

X = [ones(m, 1) X];

for t=1:m,
	a1 = X(t, :)';
	z2 = Theta1 * a1;
	a2 = [1; sigmoid(Theta1 * a1)];
	a3 = sigmoid(Theta2 * a2);
	
	columnY = zeros(num_labels, 1);
  	position = y(t, 1) + 1;
	columnY(position, 1) = 1;
	
	costOfSet = (-columnY .* log(a3)) - ((1 - columnY) .* log(1 - a3));
	J += sum(costOfSet);
	
	delta3 = a3 - columnY;
	delta2 = (Theta2(:, 2:end)' * delta3) .* sigmoidGradient(z2);
	Theta1_grad += delta2 * a1';
	Theta2_grad += delta3 * a2';
end


J /= m;

Theta1NoBias = Theta1;
Theta1NoBias(:, 1) = 0;
Theta2NoBias = Theta2;
Theta2NoBias(:, 1) = 0;

reg = (lambda / (2 * m)) * (sum(sum(Theta1NoBias .^ 2)) + sum(sum(Theta2NoBias .^ 2)));
J += reg;

grad = [Theta1_grad(:) ; Theta2_grad(:)];
end
