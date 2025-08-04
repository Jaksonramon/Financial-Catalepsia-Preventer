import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const initialCategories = [
  { name: '🏠 Rent', amount: 1150000 },
  { name: '💳 Debt repayment', amount: 380000 },
  { name: '👶 Daycare (Mango)', amount: 300000 },
  { name: '🏋️ Gym', amount: 92000 },
  { name: '🌐 Internet', amount: 98000 },
  { name: '🐶 Dog (basic)', amount: 60000 },
  { name: '🚌 Transport', amount: 120000 },
  { name: '🧴 Personal care', amount: 80000 },
  { name: '🥦 Groceries', amount: 450000 },
  { name: '🍔 Eating out', amount: 250000 },
];

export default function BudgetSidebar() {
  const [categories, setCategories] = useState(initialCategories);

  const updateAmount = (index, newAmount) => {
    const updated = [...categories];
    updated[index].amount = parseInt(newAmount) || 0;
    setCategories(updated);
  };

  const total = categories.reduce((sum, cat) => sum + cat.amount, 0);
  const budget = 3600000;
  const remaining = budget - total;

  const pieData = {
    labels: categories.map((cat) => cat.name),
    datasets: [
      {
        data: categories.map((cat) => cat.amount),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#C9CBCF', '#FFCD56', '#33FF99', '#FF6666',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="p-4 space-y-4 w-full max-w-md">
      <h2 className="text-xl font-bold">💰 Monthly Budget</h2>
      <Card>
        <CardContent className="p-4 space-y-4">
          {categories.map((cat, i) => (
            <div key={i} className="flex items-center justify-between space-x-2">
              <span>{cat.name}</span>
              <Input
                type="number"
                value={cat.amount}
                onChange={(e) => updateAmount(i, e.target.value)}
                className="w-32 text-right"
              />
            </div>
          ))}
        </CardContent>
      </Card>

      <div className="text-sm text-gray-600">
        <p>🔹 Total expenses so far: {total.toLocaleString()} COP</p>
        <p>🔹 Remaining: {remaining.toLocaleString()} COP</p>
      </div>

      <div className="mt-6">
        <h3 className="text-md font-semibold mb-2">📊 Expense Breakdown</h3>
        <Pie data={pieData} />
      </div>
    </div>
  );
}
