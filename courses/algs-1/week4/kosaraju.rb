# Kosaraju's algorithm for detecting strongly connected components
# (iterative version because the Ruby stack is sad)

$:.unshift File.expand_path('.')

require 'pp'
require 'set'

@t = 0 #finishing time
@explored = Set.new []
@finishing_time = {}

lines = IO.readlines('SCC.txt')
#lines = IO.readlines('test-oleg.txt')
#lines = ["7 1", "4 7", "1 4", "9 7", "6 9", "3 6", "9 3", "8 6", "2 8", "5 2", "8 5"]

def get_graph(lines)
	edges = {}
	nodecount = 0
	lines.each do |line|
		line.strip!
		nodes = line.split(/\s+/)
		start = nodes.shift.to_i
		nodecount = start.to_i
		if edges[start]
			edges[start].push(nodes[0].to_i)
		else
			edges[start] = [nodes[0].to_i]

		end
	end
	return edges, nodecount
end

def rev(edges,nodecount)
	reversed = {}
	edges.each do |u|
		u[1].each do |v|
			if reversed[v]
				reversed[v].push(u[0])
			else
				reversed[v] = [u[0]]
			end
			nodecount = v if v > nodecount
		end
	end
	return reversed,nodecount
end

def iter_dfs_pt1(arcs, i)
	stack = [i]
	until stack == []
		curr = stack[-1]
		if @explored.include?(curr)
			@t += 1
			@finishing_time[curr] ||= @t
			stack.pop
		else
			more = []
			@explored.add(curr)
			if arcs[curr]
				arcs[curr].each do |j|
					more.push(j) unless @explored.include?(j)
				end
			end
			if more.length == 0
				@t += 1
				@finishing_time[curr] = @t
				stack.pop
			else
				stack.concat(more)
			end
		end
	end
end

def iter_dfs_pt2(arcs, i)
	stack = [i]
	until stack == []
		curr = stack.pop
		next if @explored.include?(curr)
		@leaders[@s] += 1
		@explored.add(curr)
		if arcs[curr]
			arcs[curr].each do |j|
				stack.push(j) unless @explored.include?(j)
			end
		end
	end
end

def kosaraju(graph,nodecount)
	reversed,nodecount = rev(graph,nodecount)
	nodecount.downto(1) do |i|
		iter_dfs_pt1(reversed, i) unless @explored.include?(i)
	end
	@round2 = true
	@leaders = {}
	@s = "" #current source vertex
	@explored.clear()
	nodes = @finishing_time.sort_by { |node, time| time }
	nodes.reverse_each do |n|
		n = n[0]
		unless @explored.include?(n)
			@s = n
			@leaders[@s] = 0
			iter_dfs_pt2(graph, n)
		end
	end
end


graph, node_indexes = get_graph(lines)
kosaraju(graph, node_indexes)

leads = @leaders.sort_by { |a,b| b }

leads.each do |k,v|
	puts "leader: #{k}, size: #{v}"
end
